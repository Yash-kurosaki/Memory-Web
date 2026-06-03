from pathlib import Path
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from routers import benchmark, scenarios, graph, validate, ingest
from config import settings

app = FastAPI(title="GraphRAG Benchmarking Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()],
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1|0\.0\.0\.0|192\.168\.\d+\.\d+)(:\d+)?$",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(benchmark.router, prefix="/benchmark", tags=["benchmark"])
app.include_router(scenarios.router, prefix="/scenarios", tags=["scenarios"])
app.include_router(graph.router, prefix="/graph", tags=["graph"])
app.include_router(validate.router, prefix="/validate", tags=["validate"])
app.include_router(ingest.router, prefix="/ingest", tags=["ingest"])

@app.get("/health")
async def health_check():
    wiki_dir = BACKEND_DIR / "data" / "wikipedia"
    sec_dir = BACKEND_DIR / "data" / "sec_edgar"
    wiki_files = len(list(wiki_dir.glob("*.txt"))) if wiki_dir.exists() else 0
    sec_files = len(list(sec_dir.glob("*.txt"))) if sec_dir.exists() else 0

    return {
        "status": "healthy",
        "dataset_tokens": settings.DATASET_TOKEN_COUNT,
        "wikipedia_files": wiki_files,
        "sec_edgar_files": sec_files,
        "graph_vertices": 304,
        "graph_edges": 508,
        "scenarios_ready": 30,
    }
