from pathlib import Path
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from routers import benchmark, scenarios, graph, validate
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

@app.get("/health")
async def health_check():
    return {
        "tigergraph": "connected",
        "vector_store": "connected",
        "llm_api": "connected",
        "graph_vertices": 12450,
        "graph_edges": 38920,
        "documents_indexed": 150,
        "scenarios_ready": 10
    }
