# Render Deployment Guide

Comprehensive guide for deploying VulnerableNotes to Render.com

## 📋 Prerequisites

- Render.com account (free tier available)
- GitHub repository connected to Render
- Docker Hub images built and pushed
- All GitHub Secrets configured

## 🚀 Step-by-Step Deployment

### Step 1: Create Render Account & Connect GitHub

1. Go to [render.com](https://render.com)
2. Sign up / Log in
3. Click **"Connect GitHub"**
4. Authorize Render to access your repositories
5. Select your `vulnerable-notes` repository

### Step 2: Deploy PostgreSQL Database

#### Option A: Using Render Managed PostgreSQL (Recommended)

1. **Render Dashboard** → **New** → **PostgreSQL**
2. Fill in:
   - **Name**: `vulnerable-notes-db`
   - **Database**: `testdb`
   - **User**: `user`
   - **Region**: Choose closest to you
   - **Plan**: Free (starter for development)
3. Click **Create Database**
4. Note the **Internal Database URL** and individual credentials:
   - Hostname
   - Database
   - User
   - Password
   - Port (5432)

#### Option B: Using External PostgreSQL

If you have existing PostgreSQL:
- Use connection string format: `postgres://user:password@host:5432/database`

### Step 3: Deploy Backend Service

1. **Render Dashboard** → **New** → **Web Service**

2. **Repository Configuration:**
   - Repository: Select `vulnerable-notes`
   - Branch: `production`
   - Root Directory: `backend`

3. **Build & Deploy:**
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```bash
     gunicorn run:app -b 0.0.0.0:8081 --worker-class gthread --workers 2
     ```
   - **Region**: Same as database
   - **Plan**: Free or Starter

4. **Environment Variables** (Add all these):
   ```
   POSTGRES_DB=testdb
   POSTGRES_USER=user
   POSTGRES_PASSWORD=<get from PostgreSQL setup>
   POSTGRES_HOST=<internal database URL hostname>
   POSTGRES_PORT=5432
   FLASK_ENV=production
   FLASK_DEBUG=false
   ```

5. Click **Create Web Service**

6. **Note Service ID**: 
   - Go to Service → **Settings** → Copy **Service ID** (format: `srv-xxxxx`)
   - This is your `RENDER_BACKEND_SERVICE_ID`

7. **Wait for deployment** (5-10 minutes)

### Step 4: Deploy Frontend Service

1. **Render Dashboard** → **New** → **Static Site**

2. **Repository Configuration:**
   - Repository: Select `vulnerable-notes`
   - Branch: `production`
   - Root Directory: `frontend`

3. **Build & Deploy:**
   - **Build Command**: 
     ```bash
     npm install && npm run build
     ```
   - **Publish Directory**: `dist`
   - **Region**: Same as backend
   - **Plan**: Free

4. **Environment Variables**:
   ```
   VITE_API_BASE_URL=<your-backend-service-url>
   ```
   (Backend URL example: `https://vulnerable-notes-backend.onrender.com`)

5. Click **Create Static Site**

6. **Note Service ID**: 
   - Go to Service → **Settings** → Copy **Service ID**
   - This is your `RENDER_FRONTEND_SERVICE_ID`

7. **Wait for deployment** (2-5 minutes)

### Step 5: Configure Backend & Frontend Communication

1. **After frontend is deployed**, note the URL: `https://your-frontend-name.onrender.com`

2. **Update Backend Environment Variable**:
   - Go to Backend Service → **Settings** → **Environment**
   - Add: `FRONTEND_URL=https://your-frontend-name.onrender.com`
   - (Used for CORS configuration)

3. **Redeploy Backend**:
   - Go to Backend Service → **Deploy** → **Latest Commit**
   - OR wait for next Git push to `production` branch

4. **Update Frontend Environment Variable**:
   - After backend deployment, note the URL: `https://your-backend-name.onrender.com`
   - Go to Frontend Service → **Settings** → **Environment**
   - Update: `VITE_API_BASE_URL=https://your-backend-name.onrender.com`
   - Redeploy

### Step 6: Configure GitHub Secrets for Automated Deployment

Add these secrets to GitHub:

```
RENDER_API_KEY = <your-render-api-key>
RENDER_BACKEND_SERVICE_ID = srv-xxxxx
RENDER_FRONTEND_SERVICE_ID = srv-yyyyy
```

#### Getting Render API Key:

1. Render Dashboard → **Account Settings** → **API Keys**
2. Click **"Create API Key"**
3. Name: "GitHub Actions"
4. Copy the token → Add to GitHub Secrets

## 🔗 Connecting Frontend to Backend

### Frontend API Configuration

File: `frontend/src/main.js` or `frontend/src/config.js`

```javascript
// For development (localhost)
const API_BASE_URL = process.env.VITE_API_BASE_URL || 'http://localhost:8081';

// For production (Render)
// VITE_API_BASE_URL will be set from environment
```

### Backend CORS Configuration

File: `backend/app/application/__init__.py`

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:3000",
    "http://localhost:5173",
    os.getenv('FRONTEND_URL', 'http://localhost')
])
```

## ✅ Validation Checklist

After deployment, verify:

- [ ] **Database**: Can connect from backend service
  ```bash
  # Test via backend logs or SSH
  psql -h <host> -U <user> -d <database>
  ```

- [ ] **Backend API**: Service is running
  - Check Render logs: `curl https://backend-service.onrender.com/api/health`

- [ ] **Frontend**: Service is serving
  - Visit: `https://frontend-service.onrender.com`
  - Open browser console → No CORS errors

- [ ] **API Communication**: Frontend can reach backend
  - Open frontend in browser
  - Try making a request (login, fetch notes)
  - Check browser Network tab

- [ ] **Database**: Data is persisting
  - Make changes in app
  - Redeploy backend
  - Verify data is still there

## 🔄 Automated Deployment via GitHub Actions

Once everything is set up:

1. Push code to `production` branch
2. GitHub Actions automatically:
   - Runs tests
   - Builds Docker images
   - Pushes to Docker Hub
   - Triggers Render deployment
3. Monitor in GitHub Actions tab

## 📊 Monitoring & Logs

### View Service Logs:

1. **Render Dashboard** → Select Service
2. **Logs** tab → Real-time output
3. Look for errors or startup messages

### Check Service Health:

1. **Render Dashboard** → Service → **Health**
2. Green = Healthy
3. Red = Issues

### Database Queries:

For PostgreSQL, Render provides:
- **Render Dashboard** → Database → **Query Editor**
- Run SQL queries directly

## 🆘 Troubleshooting

### Backend Won't Start

**Check Logs** → Render Dashboard → Backend Service → Logs

Common issues:
```
❌ "ModuleNotFoundError: No module named 'flask'"
→ requirements.txt not found or wrong path
→ Build command: pip install -r requirements.txt

❌ "Connection refused to database"
→ POSTGRES_HOST is wrong
→ Database is down
→ Verify hostname from database service

❌ "Port already in use"
→ Ensure Start Command uses port from $PORT env var
→ Render: gunicorn run:app -b 0.0.0.0:$PORT
```

### Frontend Won't Load

**Check Logs** → Render Dashboard → Frontend Service → Logs

Common issues:
```
❌ "npm: command not found"
→ Node.js not installed (should be default)
→ Rebuild service

❌ "dist folder not found"
→ Build command didn't run successfully
→ Check Publish Directory is "dist"
→ Check npm run build works locally

❌ "CORS errors in console"
→ Frontend URL not in backend CORS list
→ Update CORS configuration in Flask
→ Backend must know frontend URL
```

### Database Connection Issues

```
❌ "cannot connect to database"
→ Verify POSTGRES_HOST (use internal URL, not external)
→ Verify credentials match database setup
→ Check database is running (status should be "available")

❌ "timeout connecting to database"
→ Check firewall rules
→ Verify network connectivity
→ Database might be starting up (wait a moment)
```

### API Requests Fail with 404

```
❌ "GET /api/notes returns 404"
→ Backend service not running
→ Wrong API base URL in frontend
→ Backend endpoint not implemented

→ Check backend logs
→ Verify VITE_API_BASE_URL points to correct service
```

## 🔐 Security Best Practices

- ✅ Use strong database password (Render generates one)
- ✅ Set `FLASK_DEBUG=false` in production
- ✅ Use environment variables for secrets (never commit .env)
- ✅ Enable HTTPS (Render does this automatically)
- ✅ Rotate API keys regularly

## 📈 Scaling & Optimization

### For Production:

1. **Use Paid Render Plans**:
   - More CPU/RAM for backend
   - Dedicated database
   - Auto-scaling

2. **Enable Caching**:
   - Frontend: Vite caching headers
   - Backend: Flask caching for API responses

3. **Database Optimization**:
   - Add indexes on frequently queried columns
   - Use connection pooling

4. **Monitoring**:
   - Set up error tracking (Sentry, etc.)
   - Monitor response times
   - Set up alerts for failures

## 📞 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Render PostgreSQL Guide](https://render.com/docs/databases)
- [Render Web Services](https://render.com/docs/web-services)
- [Render Environment Variables](https://render.com/docs/configure-environment)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
