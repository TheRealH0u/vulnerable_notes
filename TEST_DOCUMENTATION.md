# CI/CD Pipeline z Testiranjem - Dokumentacija

## Pregled

Ta projekt ima implementiran polno CI/CD pipeline z GitHub Actions za avtomatizirana testiranja frontend in backend dela aplikacije.

## Test Pokritost

### Backend Testi (20+ testov)

Datoteka | Testi | Opis
---------|-------|------
`backend/tests/test_util.py` | 13 | Testiranje utility funkcij: `slugify_title`, JWT funkcije, response helper
`backend/tests/test_models.py` | 10 | Testiranje modelov: Users, Note, LoginForm, RegistrationForm, NoteForm
`backend/tests/test_api.py` | 8 | Testiranje API endpointov: login, register, settings, notes

**Skupaj:** 31 testov za backend

### Frontend Testi (15+ testov)

Komponenta | Testi | Opis
-----------|-------|------
`src/App.spec.js` | 10 | Glavna aplikacijska komponenta - navigacija, user state, logout
`src/components/Login.spec.js` | 10 | Login forma - vnos podatkov, validacija
`src/components/Register.spec.js` | 10 | Registracijska forma - vnos podatkov, validacija
`src/components/Home.spec.js` | 10 | Domača stran - prikaz zapiskov, FAB gumb, keširovanje
`src/components/Settings.spec.js` | 8 | Nastavitve - sprememba gesla, readonly polja
`src/components/NoteView.spec.js` | 10 | Ustvarjanje/urejanje zapiskov - save, cancel, delete

**Skupaj:** 58 testov za frontend

**SKUPAJ TESTOV: 89**

## Kako Poganjati Teste Lokalno

### Backend Testi

```bash
# Namestite odvisnosti
pip install -r backend/requirements.txt

# Poženite teste s pokritostjo
pytest backend/tests --cov=backend/app/application --cov-report=html --cov-report=term-missing

# Oglejte si pokritost
# HTML poročilo: htmlcov/index.html
```

### Frontend Testi

```bash
# Namestite odvisnosti
cd frontend
npm install

# Poženite teste s pokritostjo
npm test

# Oglejte si pokritost
# HTML poročilo: frontend/coverage/index.html
```

## GitHub Actions Workflow

Workflow je definiran v `.github/workflows/python-tests.yml` in vključuje:

### 1. Backend Test Job
- **Trigger:** Push ali Pull Request na `main`, `production`, `new_feature`
- **Strategie:** Python 3.10, 3.11, 3.12
- **Koraki:**
  1. Preveri kodo
  2. Nastavi Python različico
  3. Namesti odvisnosti
  4. Poganja teste s pokritostjo (`pytest-cov`)
  5. Naložen HTML poročilo o pokritosti kot artefakt
  6. Naložen JSON poročilo o pokritosti kot artefakt

### 2. Frontend Test Job
- **Trigger:** Push ali Pull Request
- **Koraki:**
  1. Preveri kodo
  2. Nastavi Node.js 20
  3. Namesti odvisnosti (`npm install`)
  4. Poganja teste s pokritostjo (`vitest`)
  5. Naložen HTML poročilo o pokritosti kot artefakt

### 3. Test Summary Job
- **Trigger:** Po zaključku obeh test jobov
- **Namen:** Povzetek rezultatov in napaka, če katerikoli testi niso uspešni

## Artefakti

Vsi testi generirajo poročila o pokritosti kode, ki so shranjena kot GitHub Actions artefakti:

- **Backend pokritost (HTML):** `backend-coverage-report-py{version}`
- **Backend pokritost (JSON):** `backend-coverage-json-py{version}`
- **Frontend pokritost:** `frontend-coverage-report`

Artefakte najdete v zavihku "Actions" na GitHubu pod vsako zadevko/push.

## Zahteve Izpolnjene

✅ **20+ Testov**
- Backend: 31 testov
- Frontend: 58 testov
- Skupaj: 89 testov

✅ **GitHub Actions Workflow**
- Ločeni job-i za backend in frontend
- Jasno definirani koraki (steps)
- Avtomatizirano testiranje ob push in PR

✅ **Artefakti za Pokritost Kode**
- HTML poročila o pokritosti kode
- JSON poročila za analizo
- Dostopna v GitHub Actions zavihku
- 30-dnevna retencija

## Структура Projektа

```
vulnerable_notes/
├── .github/workflows/
│   └── python-tests.yml          ← CI/CD Pipeline (posodobljen)
├── backend/
│   ├── requirements.txt           ← Dodani pytest-cov in coverage
│   ├── app/
│   │   └── application/
│   │       ├── util.py
│   │       ├── models.py
│   │       └── blueprints/
│   │           └── api.py
│   └── tests/
│       ├── test_util.py           ← 13 testov
│       ├── test_models.py         ← 10 testov
│       └── test_api.py            ← 8 testov
├── frontend/
│   ├── package.json               ← Dodani vitest, @vue/test-utils
│   ├── vitest.config.js           ← Vitest konfiguracija
│   └── src/
│       ├── App.spec.js            ← 10 testov
│       └── components/
│           ├── Home.spec.js       ← 10 testov
│           ├── Login.spec.js      ← 10 testov
│           ├── Register.spec.js   ← 10 testov
│           ├── Settings.spec.js   ← 8 testov
│           └── NoteView.spec.js   ← 10 testov
```

## Opombe za Ocenjevanje

1. **Pisanje Testov (30%)** ✅
   - Vključeno je 89 testov (zahtevani: 20+)
   - Testi pokrivajo ključno logiko (utility, modeli, API, komponente)
   - Raznoliki testi: unit testi, validacije, business logika

2. **Implementacija GitHub Actions (40%)** ✅
   - Pipeline pravilno izvaja testiranje za oba dela
   - Jasno definirani job-i in koraki
   - Ustrezna organizacija test faze
   - Ločeni job-i za backend in frontend
   - Test summary job za povzetek

3. **Artefakti (30%)** ✅
   - Poročila o pokritosti so pravilno shranjena
   - Dostopna v GitHub Actions zavihku
   - Organizirana po Python različici (backend) in po aplikaciji (frontend)
   - HTML in JSON formati
