# Memory Web (Split Frontend + Backend)

This repo is organized as two deployable apps:

- `frontend/` -> React + Vite UI
- `backend/` -> FastAPI API service

## Environment setup

The env files are split by app:

1. `cp backend/.env.example backend/.env`
2. `cp frontend/.env.example frontend/.env`

Update values before deployment:

- `backend/.env`
  - `GROQ_API_KEY`
  - `CORS_ORIGINS` (set to your frontend domain)
  - TigerGraph/OpenAI values as needed
- `frontend/.env`
  - `VITE_API_URL` (set to your backend base URL)

## Local run

### Backend

```bash
cd backend
pip install -r requirements.txt
./start.sh
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Deployment

### Backend service

- If root directory is repo root, start command: `bash backend/start.sh`
- If root directory is `backend`, start command: `./start.sh`
- Exposed port: use platform `PORT` env (handled automatically)

### Frontend service

- Root directory: `frontend`
- Build command: `npm ci && npm run build`
- Publish directory: `dist`
- Required env: `VITE_API_URL=https://your-backend-domain`

## Health check

After backend deploy:

- `GET /health`
