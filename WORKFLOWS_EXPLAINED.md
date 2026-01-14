# 🎯 Workflow Struktura - Vulnerable Notes

## 📊 Pregled

Projekt uporablja **4 ločene GitHub Actions workflow datoteke** za optimalno organizacijo CI/CD pipeline:

```
.github/workflows/
├── tests.yml                  # ✅ Testiranje
├── deploy-development.yml     # 🔧 Development Deployment
├── deploy-production.yml      # 🚀 Production Deployment
└── deploy-pages.yml          # 📄 GitHub Pages
```

---

## 1️⃣ tests.yml - Avtomatsko Testiranje

**Namen:** Zagotavlja kakovost kode z avtomatskim testiranjem.

**Sproži se:**
- Push na katerokoli vejo (main, production, new_feature, new_feature_2)
- Pull Request na katerokoli vejo

**Jobs:**
1. **backend-tests** - Python/pytest testi z coverage
2. **frontend-tests** - Vue.js/Vitest testi z coverage
3. **test-summary** - Povzetek rezultatov testov

**Artefakti:**
- Backend coverage HTML report
- Backend coverage JSON
- Frontend coverage report

---

## 2️⃣ deploy-development.yml - Development Deployment

**Namen:** Deployment na Development okolje z Docker Hub objavami.

**Sproži se:**
- Push na vejo `main`
- Ročno (workflow_dispatch)

**Jobs:**
1. **backend-build** - Build backend aplikacije
2. **frontend-build** - Build frontend aplikacije
3. **deploy-development** - Deployment na Development environment

**Environment:** `Development` (brez manual approval)

**Docker Images:**
```
<username>/vulnerable-notes-backend:dev
<username>/vulnerable-notes-backend:dev-<commit-sha>
<username>/vulnerable-notes-frontend:dev
<username>/vulnerable-notes-frontend:dev-<commit-sha>
```

**Secrets potrebni:**
- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`

---

## 3️⃣ deploy-production.yml - Production Deployment

**Namen:** Deployment na Production okolje z ročno odobritvijo.

**Sproži se:**
- Push na vejo `production`
- Ročno (workflow_dispatch)

**Jobs:**
1. **backend-build** - Build backend aplikacije
2. **frontend-build** - Build frontend aplikacije
3. **deploy-production** - Deployment na Production environment ⚠️ **ZAHTEVA APPROVAL**

**Environment:** `Production` (zahteva manual approval!)

**Docker Images:**
```
<username>/vulnerable-notes-backend:prod
<username>/vulnerable-notes-backend:prod-<commit-sha>
<username>/vulnerable-notes-backend:latest

<username>/vulnerable-notes-frontend:prod
<username>/vulnerable-notes-frontend:prod-<commit-sha>
<username>/vulnerable-notes-frontend:latest
```

**Secrets potrebni:**
- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`
- `RENDER_BACKEND_SERVICE_ID` (opcijsko)
- `RENDER_BACKEND_API_KEY` (opcijsko)
- `RENDER_FRONTEND_SERVICE_ID` (opcijsko)
- `RENDER_FRONTEND_API_KEY` (opcijsko)

---

## 4️⃣ deploy-pages.yml - GitHub Pages Deployment

**Namen:** Posodablja statično GitHub Pages stran.

**Sproži se:**
- Push na vejo `main` ali `production`
- **Samo** ko se spremeni datoteka `index.html`
- Ročno (workflow_dispatch)

**Jobs:**
1. **deploy-github-pages** - Upload in deploy na GitHub Pages

**Environment:** `github-pages`

**Permissions:**
- `contents: read`
- `pages: write`
- `id-token: write`

---

## 🔄 Workflow Diagram

### Push na vejo `main`:
```
Push to main
├── tests.yml
│   ├── backend-tests ✅
│   ├── frontend-tests ✅
│   └── test-summary ✅
│
├── deploy-development.yml
│   ├── backend-build ✅
│   ├── frontend-build ✅
│   └── deploy-development ✅ (auto)
│
└── deploy-pages.yml (samo če index.html spremenjen)
    └── deploy-github-pages ✅ (auto)
```

### Push na vejo `production`:
```
Push to production
├── tests.yml
│   ├── backend-tests ✅
│   ├── frontend-tests ✅
│   └── test-summary ✅
│
├── deploy-production.yml
│   ├── backend-build ✅
│   ├── frontend-build ✅
│   └── deploy-production ⏸️ (čaka approval)
│       └── [Po odobritvi] ✅
│
└── deploy-pages.yml (samo če index.html spremenjen)
    └── deploy-github-pages ✅ (auto)
```

---

## 🎯 Primer Uporabe

### Scenarij 1: Razvoj nove funkcionalnosti
```bash
git checkout -b new_feature
# ... delate spremembe ...
git push origin new_feature
# Rezultat: Zažene se samo tests.yml
```

### Scenarij 2: Deployment na Development
```bash
git checkout main
git merge new_feature
git push origin main
# Rezultat: 
# 1. tests.yml ✅
# 2. deploy-development.yml ✅ (auto)
# 3. deploy-pages.yml ✅ (če je index.html spremenjen)
```

### Scenarij 3: Deployment na Production
```bash
git checkout production
git merge main
git push origin production
# Rezultat:
# 1. tests.yml ✅
# 2. deploy-production.yml ⏸️ (čaka approval)
# 3. Pojdite v Actions → Review deployments → Approve
# 4. deploy-production.yml ✅ (po odobritvi)
# 5. deploy-pages.yml ✅ (če je index.html spremenjen)
```

### Scenarij 4: Posodobitev samo GitHub Pages
```bash
# Uredite index.html
git add index.html
git commit -m "Update project description"
git push origin main
# Rezultat:
# 1. tests.yml ✅
# 2. deploy-pages.yml ✅ (samo ta workflow)
# 3. deploy-development.yml ❌ (ne sproži se, ker ni kode sprememb)
```

---

## 📋 Checklist za Delo

### Razvoj:
- [ ] Naredite feature branch
- [ ] Implementirajte funkcionalnost
- [ ] Push - testi se avtomatično poženejo
- [ ] Merge v main ko testi uspejo

### Development Deployment:
- [ ] Merge v main vejo
- [ ] Push na main
- [ ] Počakajte, da testi uspejo
- [ ] Deploy-development se avtomatično izvede
- [ ] Preverite Docker Hub za dev images

### Production Deployment:
- [ ] Merge main v production
- [ ] Push na production
- [ ] Počakajte, da testi uspejo
- [ ] Pojdite v Actions → najdite workflow run
- [ ] Kliknite "Review deployments"
- [ ] Odobrite deployment
- [ ] Preverite Docker Hub za prod in latest images

### GitHub Pages Update:
- [ ] Uredite index.html
- [ ] Push spremembe
- [ ] Deploy-pages se avtomatično izvede
- [ ] Preverite stran na GitHub Pages URL

---

## 🚨 Pomembno!

1. **Production Environment MORA imeti Required Reviewers nastavljene** v GitHub Settings → Environments → Production
2. **DOCKER_USERNAME in DOCKER_PASSWORD** morata biti nastavljena v GitHub Secrets
3. **GitHub Pages** mora biti omogočen v Repository Settings
4. **Vsi testi morajo uspeti** preden se karkoli deploya
5. **Development deployment je avtomatičen** - brez approvals
6. **Production deployment zahteva manual approval** - varnostni ukrep

---

## 📖 Več Informacij

Za podrobnejša navodila glejte:
- [DEPLOYMENT_SETUP.md](DEPLOYMENT_SETUP.md) - Nastavitev environments
- [CI_CD_SETUP.md](CI_CD_SETUP.md) - GitHub Actions setup
- [GITHUB_SECRETS_SETUP.md](GITHUB_SECRETS_SETUP.md) - Secrets konfiguracija

---

**Datum:** Januar 2026  
**Projekt:** Vulnerable Notes  
**Avtor:** GitHub Copilot + TheRealH0u
