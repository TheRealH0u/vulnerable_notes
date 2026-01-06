# CI/CD Workflow Explanation

Detaljno razlago kako deluje GitHub Actions pipeline za projekt VulnerableNotes.

## 📊 Workflow Overview

Pipeline se aktivira na push/PR na:
- `main` branch
- `production` branch
- `new_feature` branch

## 🔄 Pipeline Phases

### Phase 1: Testing (Parallel)

#### Backend Tests (`backend-tests`)
```
┌─────────────────────────┐
│  Checkout Repository    │
└────────┬────────────────┘
         ↓
┌─────────────────────────┐
│ Set up Python 3.10      │
└────────┬────────────────┘
         ↓
┌─────────────────────────┐
│ Cache pip dependencies  │
│ (Key: hash of *.txt)    │
└────────┬────────────────┘
         ↓
┌─────────────────────────┐
│ Install Dependencies    │
│ -r requirements.txt     │
└────────┬────────────────┘
         ↓
┌─────────────────────────┐
│ Run pytest Tests        │
│ + Coverage Report       │
└────────┬────────────────┘
         ↓
┌─────────────────────────┐
│ Upload Coverage         │
│ HTML + JSON Reports     │
└─────────────────────────┘
```

**Key Files:**
- `backend/requirements.txt` - Python dependencies
- `backend/tests/` - Test files
- `pytest` - Testing framework with coverage

**Artifacts Generated:**
- `backend-coverage-report-py3.10/` (HTML)
- `backend-coverage-json-py3.10/` (JSON)

---

#### Frontend Tests (`frontend-tests`)
```
┌─────────────────────────┐
│  Checkout Repository    │
└────────┬────────────────┘
         ↓
┌─────────────────────────┐
│ Set up Node.js 20       │
│ Cache npm dependencies  │
└────────┬────────────────┘
         ↓
┌─────────────────────────┐
│ Install Dependencies    │
│ npm ci (or npm install) │
└────────┬────────────────┘
         ↓
┌─────────────────────────┐
│ Run vitest Tests        │
│ + Coverage Report       │
└────────┬────────────────┘
         ↓
┌─────────────────────────┐
│ Upload Coverage Report  │
│ to GitHub Artifacts     │
└─────────────────────────┘
```

**Key Files:**
- `frontend/package.json` - Node dependencies
- `frontend/src/` - Vue components & tests
- `vitest` - Testing framework

**Artifacts Generated:**
- `frontend-coverage-report/`

---

### Phase 2: Build (Parallel, After Tests Pass)

#### Backend Build (`backend-build`)
```
Runs ONLY if backend-tests = success

┌──────────────────────────┐
│ Set up Python 3.10       │
│ Cache pip dependencies   │
└────────┬─────────────────┘
         ↓
┌──────────────────────────┐
│ Install Dependencies     │
└────────┬─────────────────┘
         ↓
┌──────────────────────────┐
│ Create build/ directory  │
└────────┬─────────────────┘
         ↓
┌──────────────────────────┐
│ Copy application files   │
│ app/ + requirements.txt  │
└────────┬─────────────────┘
         ↓
┌──────────────────────────┐
│ Upload Artifact          │
│ backend-build/ (7 days)  │
└──────────────────────────┘
```

**Artifacts Generated:**
- `backend-build/` - Ready-to-deploy Python package

---

#### Frontend Build (`frontend-build`)
```
Runs ONLY if frontend-tests = success

┌──────────────────────────┐
│ Set up Node.js 20        │
│ Cache npm dependencies   │
└────────┬─────────────────┘
         ↓
┌──────────────────────────┐
│ npm ci                   │
│ (Install dependencies)   │
└────────┬─────────────────┘
         ↓
┌──────────────────────────┐
│ npm run build            │
│ (Vite build - creates    │
│  optimized dist/)        │
└────────┬─────────────────┘
         ↓
┌──────────────────────────┐
│ Upload Artifact          │
│ frontend-build/dist/     │
│ (7 days retention)       │
└──────────────────────────┘
```

**Artifacts Generated:**
- `frontend-build/` - Vite built SPA (dist folder)

---

### Phase 3: Docker Build & Push

Runs ONLY if:
- ✅ Both builds succeed
- ✅ Branch = `main` OR `production`

```
┌───────────────────────────────────┐
│ Set up Docker Buildx              │
│ (Advanced Docker builds)          │
└────────┬────────────────────────┘
         ↓
┌───────────────────────────────────┐
│ Login to Docker Hub               │
│ (DOCKER_USERNAME + PASSWORD)      │
└────────┬────────────────────────┘
         ↓
┌───────────────────────────────────┐
│ Extract Metadata                  │
│ - Backend image tags              │
│ - Frontend image tags             │
│ (branch, semver, git sha, latest) │
└────────┬────────────────────────┘
         ↓
┌───────────────────────────────────┐
│ Build & Push Backend Image        │
│ - Context: ./backend              │
│ - Dockerfile: backend/Dockerfile  │
│ - Cache: GitHub Actions cache     │
│ - Tags: latest, branch, sha       │
└────────┬────────────────────────┘
         ↓
┌───────────────────────────────────┐
│ Build & Push Frontend Image       │
│ - Context: ./frontend             │
│ - Dockerfile: frontend/Dockerfile │
│ - Multi-stage build               │
│ - Cache: GitHub Actions cache     │
│ - Tags: latest, branch, sha       │
└────────┬────────────────────────┘
         ↓
┌───────────────────────────────────┐
│ Log Success Messages              │
│ (Image URLs printed to logs)      │
└───────────────────────────────────┘
```

**Generated Docker Images on Docker Hub:**
- `docker.io/username/vulnerable-notes-backend:latest`
- `docker.io/username/vulnerable-notes-backend:production` (if on production)
- `docker.io/username/vulnerable-notes-frontend:latest`
- `docker.io/username/vulnerable-notes-frontend:production` (if on production)

---

### Phase 4: Deployment to Render

Runs ONLY if:
- ✅ Docker build & push succeeds
- ✅ Branch = `production` (NOT main)

```
┌─────────────────────────────────┐
│ Trigger Backend Deployment      │
│ Render API: deploy service      │
│ (RENDER_API_KEY +               │
│  RENDER_BACKEND_SERVICE_ID)     │
└────────┬────────────────────────┘
         ↓
┌─────────────────────────────────┐
│ Trigger Frontend Deployment     │
│ Render API: deploy service      │
│ (RENDER_API_KEY +               │
│  RENDER_FRONTEND_SERVICE_ID)    │
└────────┬────────────────────────┘
         ↓
┌─────────────────────────────────┐
│ Log Deployment Status           │
│ "Deployment Initiated"          │
│ Monitor at dashboard.render.com │
└─────────────────────────────────┘
```

---

### Phase 5: Test Summary

Runs ALWAYS (even if tests fail) to report status:

```
┌─────────────────────────────────┐
│ Generate Summary Report         │
│ - Backend Tests: [status]       │
│ - Frontend Tests: [status]      │
│ - Backend Build: [status]       │
│ - Frontend Build: [status]      │
│                                 │
│ Exit Code:                      │
│ - 0 (success) if all pass       │
│ - 1 (fail) if any test fails    │
└─────────────────────────────────┘
```

---

## 🔐 Secrets Used

The workflow uses these GitHub Secrets:

| Secret | Usage | Phase |
|--------|-------|-------|
| `DOCKER_USERNAME` | Docker Hub login | Docker Build |
| `DOCKER_PASSWORD` | Docker Hub token | Docker Build |
| `RENDER_API_KEY` | Render deployments | Deployment |
| `RENDER_BACKEND_SERVICE_ID` | Backend service | Deployment |
| `RENDER_FRONTEND_SERVICE_ID` | Frontend service | Deployment |

---

## 💾 Caching Strategy

### Python Dependencies Cache
- **Path:** `~/.cache/pip`
- **Key:** `ubuntu-pip-{hash of requirements.txt}`
- **Benefit:** Speed up pip install if requirements haven't changed
- **Invalidation:** Automatically rebuilds if `requirements.txt` changes

### npm Dependencies Cache
- **Path:** Auto-managed by actions/setup-node
- **Key:** Hash of `package-lock.json` (or `package.json`)
- **Benefit:** Speed up npm install
- **Invalidation:** Rebuilds if packages change

### Docker Layer Cache
- **Type:** GitHub Actions cache
- **Benefit:** Reuse built layers between builds
- **Strategy:** Cache-from GHA, cache-to GHA with max mode
- **Benefit:** 50-70% faster Docker builds

---

## 📦 Artifacts Retention

| Artifact | Retention | Purpose |
|----------|-----------|---------|
| Backend Coverage | 30 days | Historical reports |
| Frontend Coverage | 30 days | Historical reports |
| Backend Build | 7 days | Deploy/debug |
| Frontend Build | 7 days | Deploy/debug |

Artifacts can be downloaded from **Actions** tab → **Specific Run** → **Artifacts**

---

## 🚦 Workflow Status Checks

GitHub shows status on PR/Commit:

```
✅ Backend Tests - PASS
✅ Frontend Tests - PASS
✅ Backend Build - PASS
✅ Frontend Build - PASS
✅ Docker Build & Push - PASS (if on main/production)
✅ Deploy to Render - PASS (if on production)
✅ Test Summary - PASS

→ Merge allowed (all checks passed)
```

If ANY job fails:
```
❌ Backend Tests - FAIL
✅ Frontend Tests - PASS
⏭️  Other jobs - SKIPPED

→ Merge blocked (failing checks)
```

---

## 🔄 Conditional Execution

### Backend Build runs if:
- `backend-tests.result == success` ✅

### Frontend Build runs if:
- `frontend-tests.result == success` ✅

### Docker Build runs if:
- Both builds succeed ✅
- `github.ref == 'refs/heads/production'` OR `'refs/heads/main'` ✅

### Render Deploy runs if:
- Docker build succeeds ✅
- `github.ref == 'refs/heads/production'` ✅ (NOT main!)

### Test Summary runs:
- Always, regardless of other statuses 🔄

---

## 📊 Performance Metrics

Typical pipeline execution times (with fresh cache):

| Phase | Duration | Notes |
|-------|----------|-------|
| Checkout | ~5s | GitHub repo download |
| Setup (Python/Node) | ~15s | Install runtime |
| Cache | ~10s | Check/restore cache |
| Install Dependencies | ~30-60s | First run longer |
| Tests | ~1-2m | depends on test count |
| Build | ~30-60s | Vite build usually fast |
| Docker Build | ~2-3m | Multi-stage, push to hub |
| Deployment | ~1-2m | Render API + deploy |
| **Total** | **~8-12 minutes** | Full pipeline |

**With cache hits:**
- Subsequent runs: ~5-8 minutes
- Docker layer cache: ~2-3 minutes

---

## 🐛 Debugging Failed Workflows

### View Detailed Logs:
1. **GitHub** → **Actions** tab
2. Click failed **Workflow Run**
3. Click job to expand
4. Click step to view logs

### Common Issues & Solutions:

#### ❌ Backend Tests Fail
- Check `backend/requirements.txt` exists
- Verify test syntax is correct
- Check test database connectivity

#### ❌ Frontend Tests Fail
- Check `frontend/package.json` is valid JSON
- Verify test files in `frontend/src/`
- Check `npm test` command in package.json

#### ❌ Docker Build Fails
- Verify Dockerfile syntax is correct
- Check context path (./backend, ./frontend)
- Verify all COPY paths exist

#### ❌ Render Deployment Fails
- Verify RENDER_API_KEY is valid
- Check SERVICE_IDs are correct (format: srv-xxxxx)
- Verify Render services exist and are accessible

---

## 📈 Monitoring & Alerts

### Recommended Monitoring:

1. **GitHub Actions Tab**
   - Monitor each workflow run
   - Check logs for errors

2. **Docker Hub Dashboard**
   - Verify images are pushed
   - Check image tags and sizes

3. **Render Dashboard**
   - Monitor service health
   - Check deployment logs
   - View runtime activity

4. **Email Notifications** (optional)
   - GitHub: Settings → Notifications
   - Configure alerts for workflow failures

---

## 🎯 Best Practices

✅ **DO:**
- Review PR checks before merging
- Check Docker Hub for successful pushes
- Monitor Render deployment status
- Keep dependencies updated
- Run tests locally before pushing

❌ **DON'T:**
- Commit secrets to repository
- Ignore failing tests
- Push directly to production without PR
- Modify workflow without testing
- Store large artifacts (>100MB)

---

## 🔗 Related Documentation

- [CI/CD Setup Guide](CI_CD_SETUP.md) - Complete setup instructions
- [Render Deployment Guide](RENDER_DEPLOYMENT.md) - Render-specific setup
- [GitHub Secrets Setup](GITHUB_SECRETS_SETUP.md) - Secret configuration
- [GitHub Actions Docs](https://docs.github.com/en/actions)

---

## ❓ FAQ

**Q: Why do some jobs skip?**
A: Jobs have `if:` conditions. Docker build only runs on main/production to save resources.

**Q: Can I run the workflow locally?**
A: Yes, use [act](https://github.com/nektos/act) to simulate GitHub Actions locally.

**Q: How do I manually trigger the workflow?**
A: GitHub Actions can be configured for manual triggers (workflow_dispatch).

**Q: Why is Docker caching important?**
A: Saves ~2 minutes per build by reusing image layers.

**Q: What if a secret is compromised?**
A: Regenerate the secret, update it in GitHub, and redeploy.
