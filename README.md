# VulnerableNotes - Frontend/Backend Split with CI/CD Pipeline

A Vue 3 + Vite frontend paired with a Flask backend, featuring a complete CI/CD pipeline with GitHub Actions, Docker Hub integration, and automated deployment to Render.

## ✨ What's Included

- **Frontend**: Vue 3 + Vite + Vitest for testing
- **Backend**: Flask + SQLAlchemy + PostgreSQL
- **CI/CD Pipeline**: GitHub Actions with:
  - Automated testing (backend + frontend)
  - Dependency caching (Python + Node.js)
  - Docker image build and push to Docker Hub
  - Automated deployment to Render
  - Health checks and monitoring

## 🚀 Quick Start (Development)

### Using Docker Compose (Recommended)

Run everything locally:

```bash
docker-compose up --build
```

This will:
- Build and run the **frontend** (Vue 3 + Nginx)
- Build and run the **backend** (Flask + Gunicorn)
- Start **PostgreSQL database** container
- Configure networking and environment variables

Access the application:
- **Frontend**: http://localhost/ (Nginx)
- **API**: http://localhost/api/* (proxied through Nginx)
- **Backend**: http://localhost:8081/ (direct)

### Frontend Development Mode

Run frontend separately in dev mode:

```bash
cd frontend
npm install
npm run dev
```

The dev server runs at http://localhost:5173. Make API requests to http://localhost:8081 (CORS is enabled for development).

## 📊 CI/CD Pipeline

This project uses **GitHub Actions** for automated testing, building, and deployment.

### Pipeline Stages

1. **Testing** → Backend (pytest) + Frontend (vitest)
2. **Build** → Backend (Python package) + Frontend (Vite bundle)
3. **Caching** → npm modules + pip dependencies
4. **Docker Build** → Build images for frontend and backend
5. **Docker Push** → Push images to Docker Hub
6. **Deploy** → Automated deployment to Render

### Setup Instructions

**[👉 Complete CI/CD Setup Guide](CI_CD_SETUP.md)**

Required GitHub Secrets:
- `DOCKER_USERNAME` - Docker Hub username
- `DOCKER_PASSWORD` - Docker Hub token
- `RENDER_API_KEY` - Render API key
- `RENDER_BACKEND_SERVICE_ID` - Render backend service ID
- `RENDER_FRONTEND_SERVICE_ID` - Render frontend service ID

### Viewing Pipeline Status

1. **GitHub**: Actions tab → Workflow runs
2. **Docker Hub**: Images tab → Pushed images
3. **Render**: Dashboard → Service logs and status

## 🏗️ Architecture

```
Frontend (Vue 3 + Vite)
    ↓
Nginx (reverse proxy)
    ↓
Backend (Flask API)
    ↓
PostgreSQL Database
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pip install -r requirements.txt
pytest tests/ --cov=app/application
```

### Frontend Tests

```bash
cd frontend
npm install
npm test
```

## 📦 Build Artifacts

After pipeline execution, artifacts are available in GitHub Actions:
- **Backend Coverage** - HTML coverage report
- **Frontend Coverage** - Vitest coverage report
- **Frontend Build** - dist/ folder (7-day retention)
- **Backend Build** - Python package (7-day retention)

## 🌐 Deployment

The application is deployed to **Render.com**:
- **Backend API**: Runs Flask application with Gunicorn
- **Frontend**: Serves Vue SPA via Nginx
- **Database**: PostgreSQL instance

Deployments are triggered automatically on pushes to `production` branch.

### Environment Variables

Configure these on Render for database connectivity:
- `POSTGRES_DB` - Database name
- `POSTGRES_USER` - Database user
- `POSTGRES_PASSWORD` - Database password
- `POSTGRES_HOST` - Database host
- `POSTGRES_PORT` - Database port (default: 5432)

## 📝 Next Steps

- Migrate Flask templates to Vue components
- Wire frontend components to `/api/*` endpoints
- Configure environment variables for your deployment
- Set up GitHub Secrets for CI/CD pipeline
- Monitor application health in Render dashboard
