# CI/CD Pipeline Setup Guide

Navodila za nastavitev celotnega CI/CD pipeline-a z GitHub Actions, Docker Hub in Render deployment.

## 📋 Pregled Pipeline-a

Avtomatiziran pipeline za testiranje, gradnjo, Docker sliko in deployment aplikacije:

```
┌─────────────────┐
│  Code Push/PR   │
│ na main/prod    │
└────────┬────────┘
         ↓
   ┌──────────────────────────────────────────┐
   │  1️⃣  TESTING (Parallel)               │
   │  • Backend: pytest + coverage           │
   │  • Frontend: vitest + coverage          │
   │  ✅ Tests + Artifacts                   │
   └────────┬─────────────────────────────────┘
            ↓
   ┌──────────────────────────────────────────┐
   │  2️⃣  BUILD (Parallel)                  │
   │  • Backend: Python package              │
   │  • Frontend: Vite SPA (dist/)           │
   │  ✅ Build Artifacts                     │
   └────────┬─────────────────────────────────┘
            ↓
   ┌──────────────────────────────────────────┐
   │  3️⃣  DOCKER BUILD & PUSH              │
   │  • Build images (with layer cache)      │
   │  • Push to Docker Hub                   │
   │  ✅ Images on Docker Hub                │
   └────────┬─────────────────────────────────┘
            ↓
   ┌──────────────────────────────────────────┐
   │  4️⃣  DEPLOY (Production only)         │
   │  • Trigger Render deployment            │
   │  • Backend + Frontend                   │
   │  ✅ App Live on Render                  │
   └──────────────────────────────────────────┘
```

## 🔧 Nastavitev GitHub Secrets

Dodajte naslednje secrets v vašem GitHub repozitoriju:
**Settings → Secrets and variables → Actions → New repository secret**

### Obvezni Secrets:

1. **`DOCKER_USERNAME`**
   - Vaše Docker Hub uporabniško ime
   - Primer: `your-docker-username`

2. **`DOCKER_PASSWORD`**
   - Vaš Docker Hub token (priporočeno) ali geslo
   - [Generiraj token: Docker Hub → Account Settings → Security](https://hub.docker.com/settings/security)

3. **`RENDER_API_KEY`**
   - Vaš Render API ključ za avtomatizirane deploymente
   - [Pridobi na Render.com → Account Settings → API Keys](https://dashboard.render.com/account/api-keys)

4. **`RENDER_BACKEND_SERVICE_ID`**
   - Service ID vašega backend-a na Renderu
   - Primer: `srv-abc123xyz456`
   - [Pridobi iz Render dashboard-a → Service → Settings]

5. **`RENDER_FRONTEND_SERVICE_ID`**
   - Service ID vašega frontend-a na Renderu
   - Primer: `srv-def789uvw012`
   - [Pridobi iz Render dashboard-a → Service → Settings]

### Nastavljanje Secrets:
```bash
# Primer dodajanja secretov prek GitHub CLI
gh secret set DOCKER_USERNAME --body "your-username"
gh secret set DOCKER_PASSWORD --body "your-token"
gh secret set RENDER_API_KEY --body "your-render-api-key"
gh secret set RENDER_BACKEND_SERVICE_ID --body "srv-xxxx"
gh secret set RENDER_FRONTEND_SERVICE_ID --body "srv-yyyy"
```

## 🐳 Docker Hub Nastavitev

### 1. Pridobi Docker Hub Account
- Registracija na [Docker Hub](https://hub.docker.com/)
- Verifikacija e-maila

### 2. Kreiraj Personal Access Token
```
Docker Hub → Account Settings → Security → New Access Token
- Ime: "GitHub Actions"
- Dostop: Read, Write, Delete
- Kopiraj token → GitHub Secrets (DOCKER_PASSWORD)
```

### 3. Preverjanje Image-ov
Po prvem uspešnem pipeline-u:
```bash
docker pull docker.io/your-username/vulnerable-notes-backend:production
docker pull docker.io/your-username/vulnerable-notes-frontend:production
```

## 🚀 Render Nastavitev

### 1. Kreiraj Backend Service na Renderu

```
Render Dashboard → New → Web Service

- Repository: Vaš GitHub repo
- Branch: production
- Build Command: 
  docker pull docker.io/your-username/vulnerable-notes-backend:latest && \
  docker tag docker.io/your-username/vulnerable-notes-backend:latest myapp-backend:latest
- Start Command: docker run -d -p 8081:8081 myapp-backend:latest

Environment Variables:
- POSTGRES_DB: (vaša DB)
- POSTGRES_USER: (vaš user)
- POSTGRES_PASSWORD: (vaša password)
- POSTGRES_HOST: (vaš host)
```

### 2. Kreiraj Frontend Service na Renderu

```
Render Dashboard → New → Static Site

- Repository: Vaš GitHub repo
- Branch: production
- Build Command: npm run build (postavka se naredi v pipeline-u)
- Publish Directory: frontend/dist
```

### 3. Pridobi Service ID-je
```
Za vsak service:
1. Odpri service na Render-u
2. Settings → Service ID
3. Kopiraj ID (npr. srv-abc123xyz)
4. Dodaj v GitHub Secrets
```

## 📊 Pipeline Sprožilni Pogoji

Pipeline se avtomatsko sprožи na:
- ✅ **Push** na `main`, `production`, `new_feature` branches
- ✅ **Pull Request** na omenjene branche

## 🔍 Monitoriranje Pipeline-a

### V GitHub repozitoriju:
1. **Actions Tab** → Preglej vse workflows
2. **Klikni na task** → Podrobnosti izvajanja
3. **Artefakti** → Download coverage reportov

### Docker Hub:
1. **Odpri Docker Hub account**
2. **Repositories** → Preveri slike in tage
3. **Activity** → Push istorija

### Render:
1. **Dashboard** → Odpri service
2. **Logs** → Preglej deployment logove
3. **Status** → Preveri zdravje aplikacije

## 📦 Artefakti Pipeline-a

Ko se pipeline izvršи, so na voljo naslednji artefakti:

| Artefakt | Pot | Retenčni DNI |
|----------|-----|-------------|
| Backend Coverage | `backend-coverage-report-py3.10/` | 30 dni |
| Frontend Coverage | `frontend-coverage-report/` | 30 dni |
| Backend Build | `backend-build/` | 7 dni |
| Frontend Build (dist) | `frontend-build/` | 7 dni |

## 🧪 Lokalno Testiranje

Pred push-om preverite lokalno:

```bash
# Backend
cd backend
pip install -r requirements.txt
pytest tests/

# Frontend
cd frontend
npm install
npm test
npm run build
```

## 🔐 Best Practices

✅ **Varnost:**
- Nikoli ne dajajte secret-ov v kod
- Redno rotirajte Docker Hub tokene
- Uporabite enterprise token za dostop, ne osebnih gesel

✅ **Performance:**
- GitHub Actions cache zmanjšuje build čas
- Docker layer cache izboljšuje Docker gradnje
- npm ci (instead of npm install) za stabilnost

✅ **Reliability:**
- Health check-ovi zagotavljajo dostopnost
- Artifact retention politik zmanjšuje storage
- Branch-based triggering preprečuje neželjene deploymente

## 🐛 Troubleshooting

### Pipeline pada na Build koraku
```
→ Preverite Python/Node verzije
→ Preverite requirements.txt/package.json
→ Lokalno testirajte build: npm run build / pytest
```

### Docker Push ne uspeva
```
→ Preverite DOCKER_USERNAME in DOCKER_PASSWORD secrets
→ Preverite Docker Hub dostop in tokene
→ Preverite da ste na production branch-i
```

### Render Deployment ne uspeva
```
→ Preverite RENDER_API_KEY je validen
→ Preverite RENDER_SERVICE_ID-je so pravilni
→ Preverite environment spremenljivke na Renderu
→ Preverite DB conexion stringe
```

### Health Check opozorilo
```
→ Aplikacija potrebuje časa da se zagotovi
→ Preverite da sta backend in frontend dostopna
→ Preverite network povezanost
```

## 📝 Dodatne Konfiguracije

### Prilagoditev Docker slik

**Backend (backend/Dockerfile):**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ .
EXPOSE 8081
CMD ["gunicorn", "run:app", "-b", "0.0.0.0:8081"]
```

**Frontend (frontend/Dockerfile):**
```dockerfile
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:stable-alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Prilagoditev Cache Ključev

Ključi se avtomatsko regenerirajo ko se spremenijo:
- `requirements.txt` → Python cache
- `package-lock.json` → Node cache
- Docker multi-stage builds → Automatic layer cache

## ✅ Validacija Setup-a

Preverka da je vse nastavljeno:

```bash
# 1. Secrets nastavljeni?
gh secret list

# 2. Dockerfile-ovi obstajajo?
ls backend/Dockerfile frontend/Dockerfile

# 3. docker-compose.yml za lokalno testiranje?
docker-compose up

# 4. Testovi lokalno delujejo?
cd backend && pytest tests/
cd frontend && npm test
```

## 🎯 Naslednji Koraki

1. ✅ Postavite vse GitHub Secrets
2. ✅ Naredite Docker Hub account
3. ✅ Postavite Render services
4. ✅ Push na production branch
5. ✅ Monitorujte Actions tab
6. ✅ Preverite Docker Hub slike
7. ✅ Testirajte aplikacijo na Renderu

---

## 📞 Pomoč

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Docker Hub Docs](https://docs.docker.com/docker-hub/)
- [Render Docs](https://render.com/docs)
