# 🔍 SonarCloud Setup - Vulnerable Notes

## 📋 Pregled

Ta dokument opisuje nastavitev **SonarCloud** za analizo kakovosti kode in uvedbo kakovostnih pregrad (quality gates) v CI/CD pipeline.

---

## 🚀 1. Nastavitev SonarCloud

### Korak 1: Prijavite se na SonarCloud

1. Pojdite na: https://sonarcloud.io/
2. Kliknite **"Log in"** in izberite **"With GitHub"**
3. Avtorizirajte SonarCloud dostop do GitHub računa

### Korak 2: Ustvarite projekt

1. Kliknite na **"+"** (zgoraj desno) → **"Analyze new project"**
2. Izberite vaš repository: **`TheRealH0u/vulnerable_notes`**
3. Kliknite **"Set Up"**

### Korak 3: Pridobite ključe

Po ustvaritvi projekta boste dobili:

- **Project Key:** `TheRealH0u_vulnerable_notes`
- **Organization Key:** `therealh0u`

### Korak 4: Ustvarite SONAR_TOKEN

1. V SonarCloud pojdite na: **My Account** (ikona profila) → **Security**
2. V **Tokens** sekciji:
   - **Name:** `GitHub Actions - vulnerable_notes`
   - **Type:** `Project Analysis Token`
   - **Project:** `TheRealH0u_vulnerable_notes`
3. Kliknite **"Generate"**
4. **POMEMBNO:** Kopirajte token - prikazan bo samo enkrat!

### Korak 5: Dodajte token v GitHub Secrets

1. V GitHub repository pojdite na: **Settings → Secrets and variables → Actions**
2. Kliknite **"New repository secret"**
3. **Name:** `SONAR_TOKEN`
4. **Value:** Prilepite token iz koraka 4
5. Kliknite **"Add secret"**

---

## 📄 2. Konfiguracija

### sonar-project.properties

Datoteka `sonar-project.properties` je že ustvarjena v korenskem imeniku projekta.

**Pomembne nastavitve:**
```properties
sonar.projectKey=TheRealH0u_vulnerable_notes
sonar.organization=therealh0u
sonar.sources=backend,frontend
sonar.exclusions=**/node_modules/**, **/dist/**, **/tests/**
sonar.python.coverage.reportPaths=backend/coverage.xml
sonar.javascript.lcov.reportPaths=frontend/coverage/lcov.info
```

**Če je vaš username/organization drugačen, posodobite:**
1. `sonar-project.properties` - spremeni `projectKey` in `organization`
2. `.github/workflows/sonarcloud-analysis.yml` - spremeni `-Dsonar.projectKey` in `-Dsonar.organization`
3. `.github/workflows/deploy-production.yml` - spremeni URL v quality gate check

---

## 🔄 3. CI/CD Pipeline Integration

### Workflow Datoteke

Projekt ima zdaj nov workflow: **`sonarcloud-analysis.yml`**

**Struktura:**
```
.github/workflows/
├── tests.yml                      # ✅ Unit testi
├── sonarcloud-analysis.yml        # 🔍 SonarCloud analiza (NEW!)
├── deploy-development.yml         # 🔧 Dev deployment
├── deploy-production.yml          # 🚀 Prod deployment (posodobljen!)
└── deploy-pages.yml              # 📄 GitHub Pages
```

### Kako deluje:

#### Za vse veje (main, production, feature):
```
Push/PR
└── sonarcloud-analysis.yml
    ├── backend-coverage ✅ (pytest z coverage)
    ├── frontend-coverage ✅ (vitest z coverage)
    ├── sonarcloud-analysis ✅ (SonarCloud scan)
    ├── quality-gate ✅ (preverjanje kakovosti)
    └── analysis-summary ✅ (povzetek)
```

#### Za production deployment:
```
Push to production
├── tests.yml ✅
├── sonarcloud-analysis.yml ✅
└── deploy-production.yml
    ├── quality-gate-check ⚠️ (PREVERI ali quality gate passed)
    ├── backend-build (samo če QG passed)
    ├── frontend-build (samo če QG passed)
    └── deploy-production ⏸️ (manual approval)
```

---

## 🎯 4. Quality Gates

### Kaj so Quality Gates?

Quality Gates so **kakovostne pregrade**, ki določajo minimalne standarde za kodo:

- **Code Coverage:** % pokritosti s testi
- **Duplications:** % podvojene kode
- **Bugs:** Št. odkritih napak
- **Vulnerabilities:** Št. varnostnih ranljivosti
- **Code Smells:** Št. težav z vzdrževanjem kode
- **Security Hotspots:** Potencialne varnostne težave

### Privzete Quality Gate nastavitve (SonarCloud):

- ✅ **Coverage:** ≥ 80%
- ✅ **Duplications:** ≤ 3%
- ✅ **New Bugs:** 0
- ✅ **New Vulnerabilities:** 0
- ✅ **Security Rating:** ≥ A

### Kako delujejo v projektu:

1. **Avtomatska analiza:** Ko pushaš kodo, se zažene `sonarcloud-analysis.yml`
2. **Preverjanje:** SonarCloud preveri vse metrike
3. **Quality Gate Status:**
   - ✅ **PASSED** - Vsi pogoji izpolnjeni
   - ❌ **FAILED** - Nekateri pogoji niso izpolnjeni

4. **Production Deployment:**
   - Če QG **PASSED** → Deployment lahko nadaljuje
   - Če QG **FAILED** → **Deployment je blokiran!** ⛔

---

## 🧪 5. Testiranje

### Test 1: Zagon SonarCloud analize

```bash
git checkout main
# Naredite spremembo v kodi
git add .
git commit -m "Test SonarCloud analysis"
git push origin main
```

**Kaj se zgodi:**
1. Zažene se `sonarcloud-analysis.yml`
2. Izvede se analiza kode
3. Rezultati so vidni v SonarCloud dashboardu

**Preverite:**
- GitHub Actions → workflow "SonarCloud Analysis"
- https://sonarcloud.io/dashboard?id=TheRealH0u_vulnerable_notes

### Test 2: Quality Gate v Production

```bash
git checkout production
git merge main
git push origin production
```

**Kaj se zgodi:**
1. Zažene se `deploy-production.yml`
2. **Prvi korak:** Quality Gate Check
3. Če QG PASSED → nadaljuje z buildanjem
4. Če QG FAILED → deployment se prekine

**Preverite:**
- GitHub Actions → workflow "Deploy to Production"
- Job "Verify Quality Gate" mora biti uspešen

---

## 📊 6. Ogled Rezultatov

### SonarCloud Dashboard

Pojdite na: https://sonarcloud.io/dashboard?id=TheRealH0u_vulnerable_notes

**Kaj vidite:**
- 📈 **Overview:** Splošna kakovost projekta
- 🐛 **Issues:** Seznam odkritih težav
- 📊 **Measures:** Podrobne metrike
- 🔒 **Security:** Varnostne ranljivosti
- 📝 **Code:** Pregled kode

### GitHub Actions

V GitHub Actions tab vidite:
- ✅/❌ Status vsakega workflow runa
- 📊 Summary z rezultati
- 🔗 Link do SonarCloud dashboarda

---

## ⚙️ 7. Konfiguracijske Možnosti

### Sprememba Quality Gate nastavitev

V SonarCloud:
1. Pojdite na projekt → **Quality Gates**
2. Lahko uporabite privzete ali ustvarite custom
3. **Administration → Quality Gates** za urejanje

### Izključitev datotek iz analize

Uredite `sonar-project.properties`:
```properties
sonar.exclusions=**/node_modules/**, \
                 **/dist/**, \
                 **/specific_file.py
```

### Prilagoditev coverage threshold

V SonarCloud:
1. **Quality Gates → Conditions**
2. Uredite "Coverage on New Code" pogoj
3. Nastavite želeno vrednost

---

## 🚨 8. Troubleshooting

### Problem: "Invalid token" ali "Unauthorized"

**Rešitev:**
1. Preverite, da je `SONAR_TOKEN` pravilno nastavljen v GitHub Secrets
2. Regenerirajte token v SonarCloud če je potekel
3. Posodobite secret v GitHubu

### Problem: "Coverage report not found"

**Rešitev:**
1. Preverite, da testi generirajo coverage reporte:
   - Backend: `backend/coverage.xml`
   - Frontend: `frontend/coverage/lcov.info`
2. Preverite `sonar-project.properties` coverage paths

### Problem: Quality Gate always fails

**Rešitev:**
1. Pojdite v SonarCloud dashboard
2. Poglejte **Why did the Quality Gate fail?**
3. Popravite kodo glede na povratne informacije
4. Push again

### Problem: "Project not found"

**Rešitev:**
1. Preverite `sonar.projectKey` v `sonar-project.properties`
2. Preverite, da projekt obstaja v SonarCloud
3. Preverite `organization` key

---

## ✅ 9. Checklist za Oddajo

- [ ] SonarCloud projekt je ustvarjen
- [ ] SONAR_TOKEN je dodan v GitHub Secrets
- [ ] `sonar-project.properties` je pravilno konfiguriran
- [ ] `sonarcloud-analysis.yml` workflow deluje
- [ ] SonarCloud analiza uspešno poteka
- [ ] Rezultati so vidni v SonarCloud dashboardu
- [ ] Quality Gate check je integriran v production deployment
- [ ] Quality Gate blokira deployment če ni passed
- [ ] Backend coverage je pravilno poslan v SonarCloud
- [ ] Frontend coverage je pravilno poslan v SonarCloud

---

## 📖 10. Dodatni Viri

- **SonarCloud Dokumentacija:** https://docs.sonarcloud.io/
- **GitHub Actions Integration:** https://docs.sonarcloud.io/advanced-setup/ci-based-analysis/github-actions/
- **Quality Gates:** https://docs.sonarcloud.io/improving/quality-gates/
- **Coverage Reports:** https://docs.sonarcloud.io/enriching/test-coverage/overview/

---

## 🎯 Povzetek

### Kaj smo naredili:

1. ✅ **Nastavili SonarCloud projekt** in povezavo z GitHub
2. ✅ **Ustvarili `sonar-project.properties`** konfiguracijo
3. ✅ **Dodali `sonarcloud-analysis.yml`** workflow za analizo
4. ✅ **Integrirali Quality Gates** v production deployment
5. ✅ **Blokiranje deploymentov** če kakovost ni zadostna

### Rezultat:

- 🔍 **Avtomatska analiza kode** pri vsakem pushu
- 📊 **Metrike kakovosti** vidne v SonarCloud
- 🛡️ **Varnostna preverjanja** za ranljivosti
- ⛔ **Blokiranje production deploymentov** če quality gate failed
- 📈 **Kontinuirano izboljševanje** kakovosti kode

---

**Datum:** Januar 2026  
**Projekt:** Vulnerable Notes  
**Ocenjevanje:** SonarCloud (25% + 50% + 25% = 100%)
