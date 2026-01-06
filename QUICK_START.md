# 🚀 Quick Start - CI/CD Pipeline

Hitri pregled kako nastaviti CI/CD pipeline v 5 korakih.

## 📋 What's New?

✅ **Complete CI/CD Pipeline** je bil dodan z GitHub Actions  
✅ **Automated Testing** - Backend (pytest) + Frontend (vitest)  
✅ **Build & Caching** - npm + pip dependencies s caching  
✅ **Docker Images** - Avtomatski build in push na Docker Hub  
✅ **Deployment** - Avtomatski deploy na Render.com  

---

## ⚡ 5-Minute Setup

### 1️⃣ Docker Hub (5 min)
```bash
# 1. Go to hub.docker.com → Sign up
# 2. Create Personal Access Token
#    Settings → Security → New Access Token
# 3. Copy token to clipboard
```

### 2️⃣ Render.com (5 min)
```bash
# 1. Go to render.com → Sign up
# 2. Connect GitHub
# 3. Create API Key
#    Account Settings → API Keys → Create API Key
# 4. Deploy PostgreSQL
#    New → PostgreSQL
```

### 3️⃣ GitHub Secrets (2 min)
```bash
# Settings → Secrets and variables → Actions
# Add 5 secrets:
- DOCKER_USERNAME=your-docker-username
- DOCKER_PASSWORD=your-docker-token
- RENDER_API_KEY=your-render-api-key
- RENDER_BACKEND_SERVICE_ID=srv-xxxxx
- RENDER_FRONTEND_SERVICE_ID=srv-yyyyy
```

### 4️⃣ Test Locally (3 min)
```bash
# Backend
cd backend && pytest tests/

# Frontend
cd frontend && npm test

# Both
docker-compose up
```

### 5️⃣ Push to Trigger (1 min)
```bash
git add .
git commit -m "CI/CD pipeline added"
git push origin main
```

**Then watch**: GitHub Actions → Actions tab ✨

---

## 📊 Pipeline Stages

```
CODE PUSH
   ↓
┌──────────────────────────┐
│ 1. TESTING (5 min)       │
│ - Backend tests          │
│ - Frontend tests         │
└──────────────────────────┘
   ↓
┌──────────────────────────┐
│ 2. BUILD (2 min)         │
│ - Backend build          │
│ - Frontend build (Vite)  │
└──────────────────────────┘
   ↓
┌──────────────────────────┐
│ 3. DOCKER (3 min)        │
│ - Build images           │
│ - Push to Hub            │
└──────────────────────────┘
   ↓
┌──────────────────────────┐
│ 4. DEPLOY (1 min)        │
│ (production only)        │
└──────────────────────────┘
   ↓
✅ APP LIVE
```

---

## 🔍 Monitor Pipeline

**GitHub Actions**
```
Repository → Actions tab → Click latest run
```

**Docker Hub**
```
hub.docker.com → Your repositories → images pushed
```

**Render**
```
dashboard.render.com → Services → View deployment status
```

---

## 📚 Documentation

For detailed setup, see:

| File | Purpose |
|------|---------|
| [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) | **Start here** - Step by step checklist |
| [GITHUB_SECRETS_SETUP.md](GITHUB_SECRETS_SETUP.md) | How to create and add secrets |
| [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) | Detailed Render setup |
| [CI_CD_SETUP.md](CI_CD_SETUP.md) | Complete pipeline guide |
| [WORKFLOW_EXPLANATION.md](WORKFLOW_EXPLANATION.md) | How the workflow works |
| [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) | What was implemented |

---

## ✅ Checklist

- [ ] Docker Hub account created
- [ ] Docker Hub token copied
- [ ] Render account created
- [ ] GitHub Secrets added (5 total)
- [ ] Render services deployed
- [ ] `git push` to trigger pipeline
- [ ] Actions tab shows green checkmarks
- [ ] Docker images in Docker Hub
- [ ] Application live on Render

---

## 🆘 Stuck?

**Tests fail locally?**
```bash
cd backend && pip install -r requirements.txt && pytest tests/
cd frontend && npm install && npm test
```

**Docker images not pushing?**
```bash
# Check secrets:
gh secret list

# Verify they match:
# DOCKER_USERNAME = hub.docker.com username
# DOCKER_PASSWORD = access token (not password)
```

**Deployment not working?**
```bash
# Check logs at: dashboard.render.com
# Verify environment variables are set
# Check SERVICE_IDs are correct (srv-xxxxx format)
```

---

## 🎯 What Happens on Each Push

**To `main` branch:**
- ✅ Run tests
- ✅ Build application
- ✅ Build Docker images
- ✅ Push to Docker Hub
- ⏭️ Skip deployment

**To `production` branch:**
- ✅ Run tests
- ✅ Build application
- ✅ Build Docker images
- ✅ Push to Docker Hub
- ✅ Deploy to Render

---

## 📈 Performance

- **First run**: ~12 minutes
- **Subsequent runs**: ~5-8 minutes (with cache)
- **Docker with cache**: ~2-3 minutes

---

## 🎉 You're All Set!

Everything is now automated. Just:
1. Code locally
2. `git push`
3. Pipeline runs automatically
4. App deploys to Render

---

**For full setup details, follow [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)**
