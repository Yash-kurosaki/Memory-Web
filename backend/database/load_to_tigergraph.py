"""
TigerGraph Savanna Data Loader
================================
Uploads the FinancialCrimeGraph (nodes + edges from data/graph.gml)
to TigerGraph Savanna via REST++ UPSERT.

Usage:
    cd backend
    source .venv/bin/activate
    python3 database/load_to_tigergraph.py

Prerequisites:
    - TIGERGRAPH_HOST set to your Savanna hostname (e.g. xyz.i.tgcloud.io)
    - TIGERGRAPH_TOKEN set to your Savanna Bearer token
    - TIGERGRAPH_GRAPH set to FinancialCrimeGraph (default)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import networkx as nx
import requests

# Load config
BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))
from config import settings  # noqa: E402

HOST   = settings.TIGERGRAPH_HOST
TOKEN  = settings.TIGERGRAPH_TOKEN
GRAPH  = settings.TIGERGRAPH_GRAPH
PORT   = settings.TIGERGRAPH_PORT

if not HOST or HOST == "your-savanna-host":
    print("❌ ERROR: Set TIGERGRAPH_HOST in backend/.env to your Savanna hostname.")
    sys.exit(1)

if not TOKEN:
    print("❌ ERROR: Set TIGERGRAPH_TOKEN in backend/.env to your Savanna Bearer token.")
    print("   Get it from: TigerGraph Cloud → My Profile → API Tokens")
    sys.exit(1)

SCHEME   = "https" if (TOKEN or str(PORT) == "443") else "http"
BASE_URL = f"{SCHEME}://{HOST}:{PORT}"
# Savanna 4.x routes data operations under /restpp/, schema under /gsql/v1/
# Legacy CE uses /graph/ directly at the root
IS_SAVANNA = (str(PORT) == "443" or TOKEN)
RESTATUS_PREFIX = "/restpp" if IS_SAVANNA else ""
HEADERS  = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}


DATA_DIR = BACKEND_DIR / "data"
GML_FILE = DATA_DIR / "graph.gml"


def _check_connection() -> None:
    print(f"🔌 Connecting to TigerGraph at {BASE_URL} ...")
    try:
        r = requests.get(f"{BASE_URL}/echo", headers=HEADERS, timeout=10)
        if r.status_code == 200:
            print("   ✓ REST++ reachable")
            return
    except Exception:
        pass
    # Try GSQL ping
    try:
        r = requests.get(f"{BASE_URL}/api/ping", headers=HEADERS, timeout=10)
        if r.status_code == 200:
            print("   ✓ GSQL endpoint reachable")
            return
    except Exception as e:
        print(f"❌ Cannot reach TigerGraph at {BASE_URL}: {e}")
        sys.exit(1)


def _create_schema() -> None:
    """Skip schema creation — graph was created via Savanna GSQL Editor."""
    print(f"📐 Schema for '{GRAPH}' already exists (created via Savanna UI) — skipping.")


def _upsert_vertices(nx_graph: nx.DiGraph) -> int:
    """Upsert all nodes as Entity vertices."""
    print(f"📦 Uploading {nx_graph.number_of_nodes()} vertices ...")
    vertices: list[dict] = []
    for node_id, attrs in nx_graph.nodes(data=True):
        vertices.append({
            "vid": str(node_id),
            "entity_type": attrs.get("type", "Entity"),
            "risk_score": int(attrs.get("risk_score", 0)),
        })

    # Batch upsert in chunks of 100
    count = 0
    for i in range(0, len(vertices), 100):
        batch = vertices[i:i + 100]
        payload = {
            "vertices": {
                "Entity": {v["vid"]: {"entity_type": {"value": v["entity_type"]},
                                      "risk_score":   {"value": v["risk_score"]}}
                           for v in batch}
            }
        }
        r = requests.post(
            f"{BASE_URL}{RESTATUS_PREFIX}/graph/{GRAPH}",
            headers=HEADERS,
            json=payload,
            timeout=30,
        )
        if r.status_code == 200:
            count += len(batch)
        else:
            print(f"   ⚠ Vertex batch {i//100+1} error {r.status_code}: {r.text[:200]}")

    print(f"   ✓ {count} vertices upserted")
    return count


def _upsert_edges(nx_graph: nx.DiGraph) -> int:
    """Upsert all edges as RELATIONSHIP edges."""
    print(f"🔗 Uploading {nx_graph.number_of_edges()} edges ...")
    edges_list = []
    for src, tgt, data in nx_graph.edges(data=True):
        edges_list.append({
            "src": str(src),
            "tgt": str(tgt),
            "relation": data.get("relation", "LINKED"),
        })

    count = 0
    for i in range(0, len(edges_list), 100):
        batch = edges_list[i:i + 100]
        edges_dict: dict = {}
        for e in batch:
            src = e["src"]
            tgt = e["tgt"]
            rel = e["relation"]
            if src not in edges_dict:
                edges_dict[src] = {"RELATIONSHIP": {"Entity": {}}}
            if "RELATIONSHIP" not in edges_dict[src]:
                edges_dict[src]["RELATIONSHIP"] = {"Entity": {}}
            if "Entity" not in edges_dict[src]["RELATIONSHIP"]:
                edges_dict[src]["RELATIONSHIP"]["Entity"] = {}
            edges_dict[src]["RELATIONSHIP"]["Entity"][tgt] = {
                "relation": {"value": rel}
            }
        payload = {
            "edges": {
                "Entity": edges_dict
            }
        }
        r = requests.post(
            f"{BASE_URL}{RESTATUS_PREFIX}/graph/{GRAPH}",
            headers=HEADERS,
            json=payload,
            timeout=30,
        )
        if r.status_code == 200:
            count += len(batch)
        else:
            print(f"   ⚠ Edge batch {i//100+1} error {r.status_code}: {r.text[:200]}")

    print(f"   ✓ {count} edges upserted")
    return count


def _verify_load(expected_nodes: int, expected_edges: int) -> None:
    """Verify the upload by counting vertices and edges."""
    print("✅ Verifying upload ...")
    try:
        r = requests.get(
            f"{BASE_URL}{RESTATUS_PREFIX}/graph/{GRAPH}/vertices/Entity?count_only=true",
            headers=HEADERS, timeout=10,
        )
        if r.status_code == 200:
            result = r.json().get("results", [{}])
            count = result[0].get("count", "?") if result else "?"
            status = "✓" if str(count) == str(expected_nodes) else "⚠"
            print(f"   {status} Vertex count: {count} (expected {expected_nodes})")
    except Exception as e:
        print(f"   ⚠ Could not verify vertex count: {e}")

    try:
        r = requests.get(
            f"{BASE_URL}{RESTATUS_PREFIX}/graph/{GRAPH}/edges?count_only=true",
            headers=HEADERS, timeout=10,
        )
        if r.status_code == 200:
            result = r.json().get("results", [{}])
            count = result[0].get("count", "?") if result else "?"
            status = "✓" if str(count) == str(expected_edges) else "⚠"
            print(f"   {status} Edge count: {count} (expected {expected_edges})")
    except Exception as e:
        print(f"   ⚠ Could not verify edge count: {e}")


def main() -> None:
    print("=" * 60)
    print("  TigerGraph Savanna — FinancialCrimeGraph Loader")
    print("=" * 60)

    if not GML_FILE.exists():
        print(f"❌ graph.gml not found at {GML_FILE}")
        sys.exit(1)

    nx_graph = nx.read_gml(GML_FILE)
    print(f"📊 Loaded graph: {nx_graph.number_of_nodes()} nodes, {nx_graph.number_of_edges()} edges")

    _check_connection()
    _create_schema()
    n_verts = _upsert_vertices(nx_graph)
    n_edges = _upsert_edges(nx_graph)
    _verify_load(nx_graph.number_of_nodes(), nx_graph.number_of_edges())

    print()
    print("=" * 60)
    print(f"  ✅ Done! {n_verts} vertices + {n_edges} edges in TigerGraph")
    print(f"  Graph: {GRAPH} on {HOST}")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. Restart backend: the server will auto-detect TigerGraph")
    print("  2. Look for: [TigerGraph] ✓ LIVE — REST++ at ...")
    print("  3. Run a benchmark — graph_nodes will show source: TigerGraph")


if __name__ == "__main__":
    main()
