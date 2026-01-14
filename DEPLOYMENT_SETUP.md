# Deployment Navodila

## 📋 Pregled

Ta dokument opisuje nastavitev GitHub Environments in CI/CD pipeline za projekt Vulnerable Notes.

## 🔧 Struktura Workflow Datotek

Projekt uporablja **4 ločene workflow datoteke** za boljšo preglednost in upravljanje:

1. **`tests.yml`** - Avtomatsko testiranje kode
   - Backend testi (Python/pytest)
   - Frontend testi (Vue.js/Vitest)
   - Coverage reporti
   - Sproži se: push/PR na vse vejah

2. **`deploy-development.yml`** - Development deployment
   - Build backend & frontend
   - Docker push z oznako `dev`
   - Deployment na Development environment
   - Sproži se: push na `main` vejo

3. **`deploy-production.yml`** - Production deployment
   - Build backend & frontend
   - Docker push z oznako `prod` in `latest`
   - **Zahteva ročno odobritev!**
   - Deployment na Production environment
   - Sproži se: push na `production` vejo

4. **`deploy-pages.yml`** - GitHub Pages deployment
   - Posodobi statično stran
   - Sproži se: sprememba `index.html` na `main` ali `production`

## 🌐 GitHub Pages

Statična stran projekta je samodejno objavljena na GitHub Pages.

### Dostop do strani:
```
https://therealh0u.github.io/vulnerable_notes/
```

### Kaj vsebuje stran:
- Ime projekta
- Člani ekipe
- Kratek opis projekta
- Tehnologije
- Lastnosti aplikacije

## 🔧 Nastavitev GitHub Environments

### 1. Development Environment

V GitHubRepository pojdite na: **Settings → Environments → New environment**

**Ime okolja:** `Development`

**Nastavitve:**
- ✅ Deployment branch: `main` only
- ❌ Required reviewers: Ni potrebno
- ❌ Wait timer: Ni potrebno

**Secrets (če potrebno):**
- `DOCKERHUB_USERNAME` - že nastavljen na repository nivoju
- `DOCKERHUB_TOKEN` - že nastavljen na repository nivoju

### 2. Production Environment

**Ime okolja:** `Production`

**Nastavitve:**
- ✅ Deployment branch: `production` only
- ✅ **Required reviewers:** Dodajte vsaj enega člana ekipe (POMEMBNO!)
- ⏱️ Wait timer: 0 minut (opcijsko)

**Secrets (če potrebno):**
- `DOCKERHUB_USERNAME` - že nastavljen na repository nivoju
- `DOCKERHUB_TOKEN` - že nastavljen na repository nivoju

## 🚀 Deployment Pipeline

### Kako deluje:

#### Za vejo `main` (Development):
1. Push na vejo `main`
2. Zažene se 2 workflow-a:
   - **`tests.yml`** - Avtomatično testiranje
   - **`deploy-development.yml`** - Deployment
3. **Avtomatično** se izvede:
   - Backend in Frontend testi
   - Build aplikacije
   - Push Docker images z oznako `dev` na Docker Hub
   - Deployment na **Development environment**

#### Za vejo `production` (Production):
1. Push na vejo `production`
2. Zažene se 2 workflow-a:
   - **`tests.yml`** - Avtomatično testiranje
   - **`deploy-production.yml`** - Deployment
3. **⏸️ Zahteva ročno odobritev** (manual approval)
4. Po odobritvi:
   - Build aplikacije
   - Push Docker images z oznako `prod` in `latest` na Docker Hub
   - Deployment na **Production environment**
   - Opcijsko: Deploy na Render (če je konfiguriran)

#### Sprememba index.html:
1. Urejanje in push `index.html` datoteke
2. Zažene se **`deploy-pages.yml`**
3. Avtomatično deployment na **GitHub Pages**

## 🐳 Docker Images

### Development (dev):
```
username/vulnerable-notes-backend:dev
username/vulnerable-notes-backend:dev-<commit-sha>

username/vulnerable-notes-frontend:dev
username/vulnerable-notes-frontend:dev-<commit-sha>
```

### Production (prod):
```
username/vulnerable-notes-backend:prod
username/vulnerable-notes-backend:prod-<commit-sha>
username/vulnerable-notes-backend:latest

username/vulnerable-notes-frontend:prod
username/vulnerable-notes-frontend:prod-<commit-sha>
username/vulnerable-notes-frontend:latest
```

## 📝 Koraki za nastavitev

### 1. Nastavite Docker Hub Secrets

V GitHub Repository: **Settings → Secrets and variables → Actions**

Dodajte:
- `DOCKER_USERNAME`: Vaš Docker Hub uporabniško ime
- `DOCKER_PASSWORD`: Docker Hub access token

### 2. Omogočite GitHub Pages

V GitHub Repository: **Settings → Pages**

**Source:** GitHub Actions (priporočeno)

ALI

**Source:** Deploy from a branch
**Branch:** Select `gh-pages` (bo ustvarjena avtomatsko)

### 3. Ustvarite Environments

Sledite navodilom zgoraj za ustvaritev Development in Production okolij.

**POMEMBNO:** Za Production environment **morate** dodati Required reviewers!

### 4. Nastavite Branch Protection (opcijsko, priporočeno)

Za vejo `production`:
- **Settings → Branches → Add rule**
- Branch name pattern: `production`
- ✅ Require pull request reviews before merging
- ✅ Require status checks to pass

### 5. Izbrišite stare workflow datoteke (če obstajajo)

Če imate stare datoteke kot `python-tests.yml` ali `deploy.yml`, jih lahko izbrišete, saj so sedaj nadomeščene z novimi:
- `tests.yml`
- `deploy-development.yml`
- `deploy-production.yml`
- `deploy-pages.yml`

## 🧪 Testiranje

### Testiranje Tests Workflow:
```bash
git checkout main
git add .
git commit -m "Test automatic testing"
git push origin main
```

Poglejte v **Actions** tab → workflow "Tests" - testi naj bi se izvedli avtomatsko.

### Testiranje Development deployment:
```bash
git checkout main
git add .
git commit -m "Test development deployment"
git push origin main
```

Poglejte v **Actions** tab → workflow "Deploy to Development" - deployment naj bi se izvedel avtomatsko.

### Testiranje Production deployment:
```bash
git checkout production
git merge main
git push origin production
```

1. Pojdite v **Actions** tab
2. Odprite workflow run "Deploy to Production"
3. Odprite job "Deploy to Production Environment"
4. Kliknite **"Review deployments"**
5. Označite "Production" in kliknite **"Approve and deploy"**

### Testiranje GitHub Pages deployment:
```bash
# Uredite index.html
git add index.html
git commit -m "Update GitHub Pages"
git push origin main
```

Workflow "Deploy GitHub Pages" naj bi se sprožil avtomatsko samo ob spremembi index.html.

## 📊 Preverjanje deploymentov

### GitHub Pages:
Odprite: `https://therealh0u.github.io/vulnerable_notes/`

### Docker Hub:
Pojdite na: `https://hub.docker.com/u/<your-username>/`

Preverite images:
- `vulnerable-notes-backend`
- `vulnerable-notes-frontend`

Preverite tags: `dev`, `prod`, `latest`

## ⚠️ Troubleshooting

### GitHub Pages se ne objavi:
1. Preverite, da je GitHub Pages omogočen v Settings
2. Preverite, da workflow ima pravilne permissions za Pages
3. Preverite logs v Actions tab

### Docker push ne uspe:
1. Preverite, da sta DOCKERHUB_USERNAME in DOCKERHUB_TOKEN pravilno nastavljena
2. Preverite, da je token aktiven in ima write permissions
3. Preverite repository imena na Docker Hub

### Production deployment ne zahteva odobritve:
1. Preverite, da je Production environment pravilno nastavljen
2. Preverite, da ima environment nastavljene "Required reviewers"
3. Preverite, da je deployment branch nastavljen na `production` only

## 📧 Kontakt

Če imate težave, kontaktirajte člane ekipe.

## ✅ Checklist za oddajo

- [ ] GitHub Pages je objavljen in deluje
- [ ] Development environment je nastavljen (brez approvals)
- [ ] Production environment je nastavljen **z manual approval**
- [ ] Docker images se uspešno objavljajo na Docker Hub
- [ ] Dev images imajo oznako `dev` in `dev-<commit-sha>`
- [ ] Prod images imajo oznako `prod`, `prod-<commit-sha>` in `latest`
- [ ] Workflow `tests.yml` se sproži za vse veje
- [ ] Workflow `deploy-development.yml` se sproži za main vejo
- [ ] Workflow `deploy-production.yml` se sproži za production vejo
- [ ] Workflow `deploy-pages.yml` se sproži ob spremembi index.html
- [ ] Manual approval deluje za Production
- [ ] Vsi testi uspešno prehajajo (backend & frontend)

## 📁 Workflow Datoteke

```
.github/workflows/
├── tests.yml                  # Avtomatsko testiranje
├── deploy-development.yml     # Development deployment (main → dev)
├── deploy-production.yml      # Production deployment (production → prod)
└── deploy-pages.yml          # GitHub Pages (index.html spremembe)
```

## 🔄 Workflow Connections

```
Push to 'main':
  ├── tests.yml ✅ (avtomatično)
  ├── deploy-development.yml ✅ (avtomatično)
  └── deploy-pages.yml ✅ (če je index.html spremenjen)

Push to 'production':
  ├── tests.yml ✅ (avtomatično)
  ├── deploy-production.yml ⏸️ (zahteva approval)
  └── deploy-pages.yml ✅ (če je index.html spremenjen)
```
