# CI/CD Setup Checklist

Koraka po koraka vodič za popolno nastavitev CI/CD pipeline-a.

## ✅ Pre-Setup Verification

- [ ] Repository je na GitHub
- [ ] Depo ima `main` in `production` branch
- [ ] Local Docker je instaliran
- [ ] `docker-compose up` deluje lokalno
- [ ] Backend testi (`pytest`) delujejo lokalno
- [ ] Frontend testi (`npm test`) delujejo lokalno

---

## 📋 Step 1: Docker Hub Setup

- [ ] Kreiraj account na [Docker Hub](https://hub.docker.com)
- [ ] Potrdi e-mail naslov
- [ ] Pridobi Docker Hub username
  - **Where to find**: Docker Hub → Account Settings
  - **Save as**: DOCKER_USERNAME for later
- [ ] Kreiraj Personal Access Token
  - **Path**: Docker Hub → Account Settings → Security → New Access Token
  - **Name**: "GitHub Actions"
  - **Permissions**: ✅ Read, ✅ Write, ✅ Delete
  - **Copy & Save**: DOCKER_PASSWORD for later

---

## 🎯 Step 2: Render.com Setup

### Create Render Account
- [ ] Sign up na [Render.com](https://render.com)
- [ ] Connect GitHub account
- [ ] Authorize Render to access GitHub

### Create PostgreSQL Database
- [ ] **Render Dashboard** → **New** → **PostgreSQL**
- [ ] **Name**: `vulnerable-notes-db`
- [ ] **Database**: `testdb`
- [ ] **User**: `user`
- [ ] **Password**: (auto-generated, save it!)
- [ ] **Plan**: Free tier
- [ ] **Wait for creation** (1-2 minutes)
- [ ] **Save Internal Database URL** (format: `host.render.internal`)

### Deploy Backend Service
- [ ] **Render Dashboard** → **New** → **Web Service**
- [ ] **Connect Repository**: Select your GitHub repo
- [ ] **Branch**: `production`
- [ ] **Root Directory**: `backend`
- [ ] **Build Command**: `pip install -r requirements.txt`
- [ ] **Start Command**: `gunicorn run:app -b 0.0.0.0:8081 --worker-class gthread --workers 2`
- [ ] **Add Environment Variables**:
  ```
  POSTGRES_DB=testdb
  POSTGRES_USER=user
  POSTGRES_PASSWORD=<password from DB setup>
  POSTGRES_HOST=<internal database URL>
  POSTGRES_PORT=5432
  FLASK_ENV=production
  FLASK_DEBUG=false
  ```
- [ ] **Create Service**
- [ ] **Wait for deployment** (5-10 minutes)
- [ ] **Note Service ID**: Settings → Service ID (format: `srv-xxxxx`)
- [ ] **Save as**: RENDER_BACKEND_SERVICE_ID

### Deploy Frontend Service
- [ ] **Render Dashboard** → **New** → **Static Site**
- [ ] **Connect Repository**: Select your GitHub repo
- [ ] **Branch**: `production`
- [ ] **Root Directory**: `frontend`
- [ ] **Build Command**: `npm install && npm run build`
- [ ] **Publish Directory**: `dist`
- [ ] **Create Service**
- [ ] **Wait for deployment** (2-5 minutes)
- [ ] **Note Service ID**: Settings → Service ID (format: `srv-yyyyy`)
- [ ] **Save as**: RENDER_FRONTEND_SERVICE_ID

### Get Render API Key
- [ ] **Render Dashboard** → **Account Settings** → **API Keys**
- [ ] Click **Create API Key**
- [ ] **Name**: "GitHub Actions"
- [ ] **Generate**
- [ ] **Copy immediately** (won't show again!)
- [ ] **Save as**: RENDER_API_KEY

### Update Services with Correct URLs
- [ ] **Get Backend URL** from Render service (e.g., `https://vulnerable-notes-backend.onrender.com`)
- [ ] **Get Frontend URL** from Render service (e.g., `https://vulnerable-notes-frontend.onrender.com`)
- [ ] **Backend Service** → Add environment variable:
  ```
  FRONTEND_URL=https://vulnerable-notes-frontend.onrender.com
  ```
- [ ] **Frontend Service** → Add environment variable:
  ```
  VITE_API_BASE_URL=https://vulnerable-notes-backend.onrender.com
  ```
- [ ] Redeploy both services

---

## 🔐 Step 3: GitHub Secrets Setup

### Add Secrets to GitHub
- [ ] **Go to**: Repository → Settings → Secrets and variables → Actions
- [ ] **Add Secret 1**: DOCKER_USERNAME
  - **Value**: Your Docker Hub username
- [ ] **Add Secret 2**: DOCKER_PASSWORD
  - **Value**: Your Docker Hub access token
- [ ] **Add Secret 3**: RENDER_API_KEY
  - **Value**: Your Render API key
- [ ] **Add Secret 4**: RENDER_BACKEND_SERVICE_ID
  - **Value**: `srv-xxxxx` (from Render)
- [ ] **Add Secret 5**: RENDER_FRONTEND_SERVICE_ID
  - **Value**: `srv-yyyyy` (from Render)

### Verify Secrets
- [ ] Run: `gh secret list` (GitHub CLI)
- [ ] All 5 secrets should be listed:
  ```
  DOCKER_PASSWORD              Updated 2024-01-06
  DOCKER_USERNAME              Updated 2024-01-06
  RENDER_API_KEY               Updated 2024-01-06
  RENDER_BACKEND_SERVICE_ID    Updated 2024-01-06
  RENDER_FRONTEND_SERVICE_ID   Updated 2024-01-06
  ```

---

## 🚀 Step 4: Test the Pipeline

### Local Testing
- [ ] Backend tests pass locally: `cd backend && pytest tests/`
- [ ] Frontend tests pass locally: `cd frontend && npm test`
- [ ] Build backend locally: `cd backend && pip install -r requirements.txt`
- [ ] Build frontend locally: `cd frontend && npm install && npm run build`

### Push to Trigger Pipeline
- [ ] Commit all changes
- [ ] **Push to `main` branch** first (to test without deployment)
  ```bash
  git add .
  git commit -m "Add CI/CD pipeline"
  git push origin main
  ```
- [ ] Go to GitHub **Actions** tab
- [ ] Watch the workflow execute
- [ ] **Verify all steps pass**:
  - ✅ Backend Tests
  - ✅ Frontend Tests
  - ✅ Backend Build
  - ✅ Frontend Build
  - ✅ Docker Build & Push
  - ✅ (Deploy skipped for non-production branch)

### Check Docker Hub
- [ ] Go to **Docker Hub** → Your account
- [ ] **Repositories** tab
- [ ] Verify images exist:
  - [ ] `vulnerable-notes-backend` (with tag `main`)
  - [ ] `vulnerable-notes-frontend` (with tag `main`)

---

## 🌐 Step 5: Production Deployment

### Push to Production
- [ ] Create/merge PR to `production` branch
- [ ] Push to `production`:
  ```bash
  git push origin production
  ```
- [ ] Go to GitHub **Actions** tab
- [ ] Watch the workflow execute
- [ ] **Verify all steps including deployment**:
  - ✅ All tests pass
  - ✅ All builds pass
  - ✅ Docker Build & Push
  - ✅ Deploy to Render

### Verify Deployment
- [ ] Check **Render Dashboard** for service health
- [ ] Check service **Logs** for errors
- [ ] **Test Backend API**:
  ```bash
  curl https://vulnerable-notes-backend.onrender.com/api/notes
  ```
- [ ] **Test Frontend**:
  - Open https://vulnerable-notes-frontend.onrender.com in browser
  - Check for CORS errors in console
  - Try making a request (login, fetch notes)

### Verify Docker Hub
- [ ] Go to **Docker Hub** → Your repositories
- [ ] Verify images have `production` tag:
  - [ ] `vulnerable-notes-backend:production`
  - [ ] `vulnerable-notes-frontend:production`

---

## 📊 Step 6: Monitor Pipeline

### GitHub Actions
- [ ] Every push triggers workflow
- [ ] Can view logs for each step
- [ ] Can download artifacts:
  - Backend coverage report
  - Frontend coverage report
  - Build artifacts

### Docker Hub
- [ ] Images are pushed on every build
- [ ] Activity log shows push history
- [ ] Can delete old images if needed

### Render Dashboard
- [ ] Services show health status
- [ ] Logs section shows real-time output
- [ ] Can manually trigger redeploy if needed

---

## 🔧 Step 7: Optional Configurations

### Email Notifications
- [ ] **GitHub Settings** → **Notifications**
- [ ] Configure workflow failure alerts

### Database Backups
- [ ] **Render Dashboard** → **PostgreSQL Service** → **Backups**
- [ ] Enable automated backups (recommended)

### Custom Domain (Optional)
- [ ] Register domain (GoDaddy, Namecheap, etc.)
- [ ] **Render Dashboard** → Service → **Custom Domain**
- [ ] Point DNS to Render

### Environment-Specific Config
- [ ] Different configs for dev/staging/production
- [ ] Use Render environment variables for each

---

## ✅ Final Verification Checklist

### Application Functionality
- [ ] Backend API is responding
- [ ] Frontend is loading
- [ ] Frontend can communicate with backend
- [ ] Authentication works
- [ ] Database is storing data
- [ ] Logs show no errors

### Pipeline Status
- [ ] All GitHub Actions workflows complete successfully
- [ ] Docker images exist on Docker Hub
- [ ] Services deployed on Render
- [ ] Health checks pass

### Security
- [ ] No secrets committed to repository
- [ ] GitHub Secrets are configured correctly
- [ ] Database password is strong
- [ ] HTTPS is enabled (Render does this automatically)

---

## 🎯 Common Issues & Solutions

### Pipeline Won't Start
- [ ] Check webhook is enabled (GitHub → Repo → Settings → Webhooks)
- [ ] Verify branch name is exactly `main` or `production`
- [ ] Check repository permissions

### Tests Fail
- [ ] Run locally first: `pytest backend/tests/` and `npm test frontend/`
- [ ] Check error logs in GitHub Actions
- [ ] Update dependencies if needed

### Docker Push Fails
- [ ] Verify DOCKER_USERNAME and DOCKER_PASSWORD secrets are correct
- [ ] Check Docker Hub token hasn't expired
- [ ] Verify token has read/write permissions

### Render Deployment Fails
- [ ] Check RENDER_API_KEY and SERVICE_IDs are correct
- [ ] Verify database credentials match
- [ ] Check Render logs for errors
- [ ] Ensure branch is `production` (not main)

### Frontend Can't Reach Backend
- [ ] Check VITE_API_BASE_URL environment variable on Render
- [ ] Verify backend CORS configuration includes frontend URL
- [ ] Check network requests in browser DevTools

---

## 📚 Documentation Files

Created documentation for reference:

- **[CI_CD_SETUP.md](CI_CD_SETUP.md)** - Detailed CI/CD guide
- **[GITHUB_SECRETS_SETUP.md](GITHUB_SECRETS_SETUP.md)** - Secrets configuration
- **[RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)** - Render deployment guide
- **[WORKFLOW_EXPLANATION.md](WORKFLOW_EXPLANATION.md)** - Workflow detailed explanation
- **[README.md](README.md)** - Project overview

---

## 🎉 Success!

If all checkboxes are completed:

✅ **CI/CD pipeline is fully operational**
✅ **Docker images are being built and pushed**
✅ **Application is deployed on Render**
✅ **Automatic deployments on production push**

---

## 📞 Need Help?

- **GitHub Actions Issues**: Check [GitHub Actions Docs](https://docs.github.com/en/actions)
- **Docker Hub Issues**: Check [Docker Hub Docs](https://docs.docker.com/docker-hub/)
- **Render Issues**: Check [Render Docs](https://render.com/docs)
- **Workflow Details**: See [WORKFLOW_EXPLANATION.md](WORKFLOW_EXPLANATION.md)

---

**Last Updated**: January 2024
**Status**: ✅ Complete
