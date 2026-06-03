# Memory-Web — GraphRAG Financial Crime Intelligence

**Round 2 submission — GraphRAG Inference Hackathon by TigerGraph**

## Results (30-scenario benchmark)

| Metric | Score | Target |
|--------|-------|--------|
| Token reduction vs Basic RAG | **94.7%** | ≥30% |
| LLM Judge pass rate | **100.0%** | ≥90% (bonus) ✅ |
| BERTScore F1 | **0.9299** | ≥0.88 (bonus) ✅ |
| Dataset size | **913M tokens** | ≥100M |

## Stack
- **LLM**: Gemini 1.5 Flash (via REST API)
- **Graph**: TigerGraph (NetworkX fallback)
- **Vector store**: ChromaDB + FAISS
- **Dataset**: SEC EDGAR 2,982 filings + 62 Wikipedia articles
- **Evaluation**: Entity-weighted LLM judge + BERTScore approximation

## Quick start

```bash
# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env   # add GEMINI_API_KEY
python3 generate_data.py
./start.sh

# Frontend
cd frontend
npm install && npm run dev
```

## Run benchmark

```bash
cd backend
python3 generate_data.py          # build graph + vector index
python3 benchmark/run_benchmark.py --scenarios scenarios.json \
  --output ../benchmark_report.json --dataset-tokens 913931776
```

## Dataset verification

```bash
python3 data/token_counter.py --input data/ --output token_count_proof.json
# Produces: total_tokens: 913,931,776
```


