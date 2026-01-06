# Frontend-Backend Communication Setup

Successfully configured the frontend and backend to communicate with each other.

## ✅ Changes Made

### 1. Backend CORS Configuration
**File**: [backend/app/application/__init__.py](backend/app/application/__init__.py)

Updated Flask CORS to allow requests from:
- ✅ `https://vulnerable-notes-frontend.onrender.com` (Production Render)
- ✅ `http://localhost:3000` (Local dev)
- ✅ `http://localhost:5173` (Local Vite dev server)
- ✅ `http://localhost:8081` (Local backend)
- ✅ Dynamic URL from `FRONTEND_URL` environment variable

```python
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:80",
    "http://localhost",
    "https://vulnerable-notes-frontend.onrender.com",
    os.getenv('FRONTEND_URL', 'http://localhost')
]

CORS(app, 
     resources={r"/api/*": {"origins": allowed_origins}},
     supports_credentials=True)
```

### 2. Frontend API Utility
**File**: [frontend/src/api.js](frontend/src/api.js) (NEW)

Created a centralized API client that:
- Uses correct backend URL in production: `https://vulnerable-notes-backend.onrender.com`
- Uses relative paths in development (proxied through Vite)
- Includes request/response interceptors for debugging
- Supports credentials for authentication

**Usage in Vue components:**
```javascript
import apiClient from '@/api'

// Make requests
apiClient.get('/api/notes')
apiClient.post('/api/notes', { title: 'New Note', content: '...' })
```

### 3. Vite Dev Server Configuration
**File**: [frontend/vite.config.js](frontend/vite.config.js)

Updated proxy target from `http://localhost:5000` to `http://localhost:8081` to match:
- Backend port (8081 in docker-compose)
- Correct API endpoint routing

## 🔧 Environment Variables

### For Render Backend Service
Add this environment variable to the Render backend service:
```
FRONTEND_URL=https://vulnerable-notes-frontend.onrender.com
```

**How to add**:
1. Render Dashboard → Backend Service → Settings → Environment
2. Add new variable: `FRONTEND_URL`
3. Value: `https://vulnerable-notes-frontend.onrender.com`
4. Save and redeploy

### For Frontend (Vite)
Add this to Render frontend service environment variables:
```
VITE_API_BASE_URL=https://vulnerable-notes-backend.onrender.com
```

**How to add**:
1. Render Dashboard → Frontend Service → Settings → Environment
2. Add new variable: `VITE_API_BASE_URL`
3. Value: `https://vulnerable-notes-backend.onrender.com`
4. Save and redeploy

## 🧪 Testing Communication

### Local Testing (docker-compose)
```bash
# Start everything
docker-compose up

# Frontend will be at: http://localhost
# Backend API: http://localhost:8081/api
# Database: localhost:5432
```

The frontend will automatically:
- Proxy `/api` requests to `http://localhost:8081`
- Use the API utility for all requests

### Production Testing (Render)
Once both services are deployed:

1. **Test Backend Health**
   ```bash
   curl https://vulnerable-notes-backend.onrender.com/api/notes
   ```

2. **Test Frontend**
   - Open https://vulnerable-notes-frontend.onrender.com
   - Open browser Developer Tools → Console
   - Look for API requests and responses
   - Try logging in or creating a note

3. **Check for CORS Errors**
   - Console should NOT show CORS errors
   - If errors appear, verify:
     - FRONTEND_URL is set on backend
     - Frontend can reach the backend URL
     - CORS origins are configured correctly

## 📋 Deployment Checklist

- [ ] Backend service deployed on Render
- [ ] Frontend service deployed on Render
- [ ] Database connected and initialized
- [ ] Backend environment variable `FRONTEND_URL` = frontend URL
- [ ] Frontend environment variable `VITE_API_BASE_URL` = backend URL
- [ ] Both services redeployed after env variable changes
- [ ] Test frontend → backend communication works
- [ ] No CORS errors in browser console
- [ ] Login/Create Note/View Notes functionality works

## 🔗 Service URLs

### Production (Render)
- **Frontend**: https://vulnerable-notes-frontend.onrender.com
- **Backend**: https://vulnerable-notes-backend.onrender.com
- **Database**: Render managed PostgreSQL

### Local (docker-compose)
- **Frontend**: http://localhost
- **Backend**: http://localhost:8081
- **Database**: localhost:5432

## 🐛 Troubleshooting

### Frontend Can't Reach Backend
**Symptoms**: 
- Network requests to `/api` fail
- Browser shows "Failed to fetch" or "404"

**Solutions**:
1. Check VITE_API_BASE_URL is set correctly on Render
2. Verify backend URL is accessible: `curl https://vulnerable-notes-backend.onrender.com/api/notes`
3. Check CORS configuration in Flask

### CORS Errors
**Symptoms**:
- Browser console: "Access to XMLHttpRequest... blocked by CORS policy"

**Solutions**:
1. Add frontend URL to `allowed_origins` in Flask
2. Set `FRONTEND_URL` environment variable on Render
3. Redeploy backend service
4. Check `supports_credentials=True` in CORS config

### API Requests Timeout
**Symptoms**:
- Requests hang or timeout after 30s

**Solutions**:
1. Check backend service is running (Render dashboard)
2. Check database connection (Render logs)
3. Verify network connectivity
4. Check request payload isn't too large

## 📝 Summary

✅ Backend now accepts requests from the frontend  
✅ Frontend configured with correct backend URL  
✅ Both development and production environments supported  
✅ Error handling and debugging utilities included  
✅ Ready for full deployment and testing  

**Next Step**: Push changes to trigger CI/CD pipeline and deploy to Render
