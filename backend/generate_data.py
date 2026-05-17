import os
import json
import random
import faiss
import numpy as np
import networkx as nx
from faker import Faker
from sentence_transformers import SentenceTransformer

fake = Faker()
Faker.seed(42)
random.seed(42)

os.makedirs("data", exist_ok=True)

# 1. CORE SCENARIO ENTITIES
core_entities = [
    # SCN-001 (Hidden Ownership)
    {"id": "Meridian Holdings Ltd", "type": "Company", "risk": 85},
    {"id": "BVI Shell Alpha", "type": "Company", "risk": 60},
    {"id": "Kasarov Enterprises", "type": "Company", "risk": 75},
    {"id": "Viktor Kasarov", "type": "Person", "risk": 95},
    
    # SCN-002 (Sanctions Exposure / Shared Directors)
    {"id": "Vertex Capital", "type": "Company", "risk": 20},
    {"id": "Ocean Logistics", "type": "Company", "risk": 55},
    {"id": "Harbor Group", "type": "Company", "risk": 65},
    {"id": "Red Star Shipping", "type": "Company", "risk": 99},
    
    # SCN-003 (Shared Infrastructure / Cross-border)
    {"id": "Horizon Group", "type": "Company", "risk": 85},
    {"id": "123 Offshore Blvd", "type": "Address", "risk": 90},
    {"id": "Phantom Logistics", "type": "Company", "risk": 95},
    
    # SCN-004 (Shortest Laundering Chain)
    {"id": "Jonathan Doe", "type": "Person", "risk": 70},
    {"id": "Cayman Account 99X", "type": "Account", "risk": 85},
    {"id": "Apex Ventures", "type": "Company", "risk": 90},
    {"id": "Global Launderers LLC", "type": "Company", "risk": 100},
]

core_edges = [
    # SCN-001
    ("BVI Shell Alpha", "Meridian Holdings Ltd", "OWNS", "100%"),
    ("Kasarov Enterprises", "BVI Shell Alpha", "CONTROLS", "Majority"),
    ("Viktor Kasarov", "Kasarov Enterprises", "OWNS", "100%"),
    
    # SCN-002
    ("Vertex Capital", "Ocean Logistics", "FUNDED", "$5M"),
    ("Ocean Logistics", "Harbor Group", "SHARES_DIRECTOR", "Elena Rostova"),
    ("Harbor Group", "Red Star Shipping", "OWNS", "Subsidiary"),
    
    # SCN-003
    ("Horizon Group", "123 Offshore Blvd", "REGISTERED_AT", "Suite 400"),
    ("Phantom Logistics", "123 Offshore Blvd", "REGISTERED_AT", "Suite 400"),
    
    # SCN-004
    ("Jonathan Doe", "Cayman Account 99X", "WIRE_TRANSFER", "$150k"),
    ("Cayman Account 99X", "Apex Ventures", "HELD_BY", "Corporate Account"),
    ("Apex Ventures", "Global Launderers LLC", "TRANSACTED_WITH", "Shell Service")
]

core_docs = [
    # Fragmented SCN-001
    "Meridian Holdings Ltd is a logistics firm.",
    "Meridian Holdings Ltd is wholly owned by BVI Shell Alpha.",
    "BVI Shell Alpha's majority controller is Kasarov Enterprises.",
    "Viktor Kasarov is the sole owner of Kasarov Enterprises.",
    
    # Fragmented SCN-002
    "Vertex Capital funded Ocean Logistics with a $5M loan.",
    "Ocean Logistics shares directors with Harbor Group.",
    "Harbor Group owns Red Star Shipping.",
    "Red Star Shipping is currently under sanctions.",
    
    # Fragmented SCN-003
    "Horizon Group operates internationally and is registered at 123 Offshore Blvd.",
    "Phantom Logistics is a known sanctioned entity.",
    "Phantom Logistics lists its headquarters as 123 Offshore Blvd.",
    
    # Fragmented SCN-004
    "Jonathan Doe initiated a wire transfer to Cayman Account 99X.",
    "Cayman Account 99X is held by Apex Ventures.",
    "Apex Ventures frequently transacts with Global Launderers LLC.",
    
    # Fragmented SCN-005
    "Viktor Kasarov is a high-risk individual of interest.",
    "Kasarov Enterprises is wholly owned by Viktor Kasarov.",
    "BVI Shell Alpha is controlled by Kasarov Enterprises.",
    "BVI Shell Alpha owns Meridian Holdings Ltd, a logistics firm registered offshore."
]

# 2. GENERATE MASSIVE NOISE DATASET
nodes = list(core_entities)
edges = list(core_edges)
docs = [{"id": f"doc{i}", "text": text} for i, text in enumerate(core_docs)]

for i in range(300):
    ntype = random.choice(["Company", "Person", "Account", "Trust"])
    if ntype == "Company":
        name = fake.company()
    elif ntype == "Person":
        name = fake.name()
    elif ntype == "Account":
        name = f"Account {fake.bban()}"
    else:
        name = f"{fake.last_name()} Trust"
        
    nodes.append({"id": name, "type": ntype, "risk": random.randint(5, 40)})
    if random.random() > 0.5:
        docs.append({"id": f"noise{i}", "text": f"{name} is a {ntype.lower()} registered in {fake.country()}."})

all_ids = [n["id"] for n in nodes]
for i in range(500):
    u = random.choice(all_ids)
    v = random.choice(all_ids)
    if u != v:
        rel = random.choice(["TRANSACTED_WITH", "DIRECTOR_OF", "OWNS", "LOAN_PROVIDED", "PARTNER_OF"])
        edges.append((u, v, rel, f"{random.randint(10, 99)}% confidence"))

print(f"Building FAISS index with {len(docs)} documents...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")
texts = [d["text"] for d in docs]
embeddings = embedder.encode(texts)
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings, dtype=np.float32))
faiss.write_index(index, "data/vector_index.faiss")

with open("data/chunks.json", "w") as f:
    json.dump(docs, f, indent=2)

print(f"Building Graph with {len(nodes)} nodes and {len(edges)} edges...")
G = nx.DiGraph()
for n in nodes:
    G.add_node(n["id"], type=n["type"], risk_score=n["risk"])
for u, v, rel, weight in edges:
    G.add_edge(u, v, relation=rel, weight=weight)
    
nx.write_gml(G, "data/graph.gml")

# 5. NEW CHALLENGING SCENARIOS
scenarios = [
  {
    "id": "SCN-001",
    "category": "hidden_ownership",
    "query": "Who is the ultimate beneficial owner of Meridian Holdings Ltd?",
    "ground_truth": "Meridian Holdings Ltd is owned by BVI Shell Alpha, which is controlled by Kasarov Enterprises, which is owned by Viktor Kasarov.",
    "expected_graphrag_advantage": "Requires 3-hop reconstruction. Vector RAG will only retrieve BVI Shell Alpha.",
    "tags": ["ownership", "multi-hop", "shell-company"]
  },
  {
    "id": "SCN-002",
    "category": "sanctions_exposure",
    "query": "Does Vertex Capital have any indirect exposure to sanctioned entities?",
    "ground_truth": "Yes, Vertex Capital funded Ocean Logistics, which shares directors with Harbor Group, which owns the sanctioned entity Red Star Shipping.",
    "expected_graphrag_advantage": "Requires connecting loan -> shared director -> ownership. Vector RAG fails.",
    "tags": ["exposure", "multi-hop", "sanctions"]
  },
  {
    "id": "SCN-003",
    "category": "shared_infrastructure",
    "query": "What links Horizon Group to sanctioned activities?",
    "ground_truth": "Horizon Group shares a registered address (123 Offshore Blvd) with Phantom Logistics, a sanctioned entity.",
    "expected_graphrag_advantage": "Edge overlap on address. Vectors often fail to associate the two companies.",
    "tags": ["infrastructure", "address"]
  },
  {
    "id": "SCN-004",
    "category": "shortest_laundering_chain",
    "query": "What is the shortest exposure chain between Jonathan Doe and Global Launderers LLC?",
    "ground_truth": "Jonathan Doe wired money to Cayman Account 99X, held by Apex Ventures, which transacts with Global Launderers LLC.",
    "expected_graphrag_advantage": "Shortest-path graph algorithm executes directly over edges.",
    "tags": ["shortest-path", "laundering"]
  },
  {
    "id": "SCN-005",
    "category": "cross_chain_risk",
    "query": "Does Viktor Kasarov have any links to high-risk or sanctioned entities?",
    "ground_truth": "Viktor Kasarov owns Kasarov Enterprises, which controls BVI Shell Alpha, which owns Meridian Holdings Ltd — forming a 3-layer shell company structure with significant jurisdictional risk exposure.",
    "expected_graphrag_advantage": "Requires tracing a 3-hop ownership chain from a named individual to a high-risk shell network. Vector RAG retrieves individual entity documents but fails to reconstruct the chain.",
    "tags": ["ownership", "shell-company", "individual-risk", "multi-hop"]
  }
]

with open("scenarios.json", "w") as f:
    json.dump(scenarios, f, indent=2)

print("Massive dataset initialization complete!")
