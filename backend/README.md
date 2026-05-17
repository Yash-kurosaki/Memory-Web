# Backend (FastAPI)

## Environment

Copy template and set values:

```bash
cp .env.example .env
```

Important variables:

- `GROQ_API_KEY`
- `CORS_ORIGINS`
- `TIGERGRAPH_*`

## Run locally

```bash
pip install -r requirements.txt
./start.sh
```

This starts `uvicorn main:app` on `0.0.0.0:${PORT:-8000}`.

## Deploy

From repo root, use:

```bash
bash backend/start.sh
```

Or from inside `backend/`:

```bash
./start.sh
```
