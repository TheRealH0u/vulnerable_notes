# VulnerableNotes - Frontend/Backend Split

This repository was split to separate the frontend (Vue 3 + Vite) and backend (Flask).

What I changed:
- Added a `frontend/` directory with a Vite + Vue 3 app scaffold.
- Added an `api` blueprint in the Flask app exposing JSON endpoints under `/api/*` (login, notes CRUD).
- Enabled simple CORS on the Flask app for development.
 - Updated `docker-compose.yml` to build the frontend with a `frontend_builder` and serve it with an `nginx` service.

Quick start (development):

Run everything via docker-compose (recommended):

1) From repository root run (PowerShell):

   docker-compose up --build

This will perform the following:
- `frontend` will be built from `frontend/Dockerfile` and run a static file server on port 5000.
- `nginx` will serve the frontend on port 80 and proxy `/api` to the backend API.
- `vuln_notes_web` is the Flask/Gunicorn API service listening internally on port 8081.

Note: the compose file no longer creates a database container. You must provide database connection details using environment variables or a separate DB service. The backend env vars are still present in `docker-compose.yml` for convenience; point `POSTGRES_HOST`/`POSTGRES_USER`/`POSTGRES_PASSWORD` to your DB.

Routing behavior (after compose up):
- http://localhost/ -> served by nginx (the Vue SPA)
- http://localhost/api/... -> proxied by nginx to the Flask API (vuln_notes_web) on internal port 8081

If you want to run frontend in dev mode instead of building in docker:

  cd frontend
  npm install
  npm run dev

The dev server runs at http://localhost:5173 (remember the API is routed via nginx in the compose setup above; if you run the dev server separately, frontend will make API requests directly to `/api` which requires Flask CORS to be enabled; this repo enables CORS for development.)

Notes / Next steps:
- The Vue app currently includes a minimal `Home` view that calls `GET /api/notes`.
- You should migrate the other templates (`login`, `register`, `note`, `settings`) into Vue components/pages and wire them to the API endpoints in `application/blueprints/api.py`.
- For production, build the frontend (`npm run build`) and serve the static `dist/` via nginx or as static files from the Flask app.
