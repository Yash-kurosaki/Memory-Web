# Benchmark Metrics by Scenario


## SCN-001

**Query:** Who is the ultimate beneficial owner of Meridian Holdings Ltd?

- Winner: `GraphRAG`
- GraphRAG vs LLM-Only deltas: tokens `85.67%`, latency `99.48%`, cost `100.0%`, judge `4400.0%`

| Pipeline | BERT P | BERT R | BERT F1 | Judge Total | Entity | Path | Relation | Traversal | Multi-hop | Hallucination Penalty |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| LLM-Only | 0.0437 | 0.3810 | 0.0784 | 1 | 4 | 2 | 3 | 0 | 1 | -9 |
| Vector-RAG | 0.0909 | 0.1429 | 0.1111 | 2 | 4 | 2 | 3 | 0 | 2 | -9 |
| GraphRAG | 0.2941 | 0.4762 | 0.3636 | 45 | 10 | 15 | 5 | 10 | 5 | 0 |

## SCN-002

**Query:** Does Vertex Capital have any indirect exposure to sanctioned entities?

- Winner: `GraphRAG`
- GraphRAG vs LLM-Only deltas: tokens `85.28%`, latency `99.44%`, cost `100.0%`, judge `0.0%`

| Pipeline | BERT P | BERT R | BERT F1 | Judge Total | Entity | Path | Relation | Traversal | Multi-hop | Hallucination Penalty |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| LLM-Only | 0.0340 | 0.2500 | 0.0599 | 0 | 4 | 2 | 2 | 0 | 1 | -10 |
| Vector-RAG | 0.0000 | 0.0000 | 0.0000 | 0 | 2 | 0 | 0 | 0 | 0 | -6 |
| GraphRAG | 0.1143 | 0.2000 | 0.1455 | 9 | 6 | 7 | 2 | 0 | 3 | -9 |

## SCN-003

**Query:** What links Horizon Group to sanctioned activities?

- Winner: `GraphRAG`
- GraphRAG vs LLM-Only deltas: tokens `78.3%`, latency `99.81%`, cost `100.0%`, judge `0.0%`

| Pipeline | BERT P | BERT R | BERT F1 | Judge Total | Entity | Path | Relation | Traversal | Multi-hop | Hallucination Penalty |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| LLM-Only | 0.0312 | 0.4000 | 0.0580 | 0 | 6 | 2 | 0 | 0 | 1 | -10 |
| Vector-RAG | 0.1220 | 0.3333 | 0.1786 | 4 | 6 | 2 | 0 | 0 | 2 | -6 |
| GraphRAG | 0.0926 | 0.3333 | 0.1449 | 8 | 6 | 3 | 2 | 5 | 2 | -10 |

## SCN-004

**Query:** What is the shortest exposure chain between Jonathan Doe and Global Launderers LLC?

- Winner: `GraphRAG`
- GraphRAG vs LLM-Only deltas: tokens `83.81%`, latency `99.74%`, cost `100.0%`, judge `455.56%`

| Pipeline | BERT P | BERT R | BERT F1 | Judge Total | Entity | Path | Relation | Traversal | Multi-hop | Hallucination Penalty |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| LLM-Only | 0.0593 | 0.4444 | 0.1046 | 9 | 6 | 4 | 0 | 6 | 3 | -10 |
| Vector-RAG | 0.0357 | 0.0556 | 0.0435 | 0 | 2 | 0 | 0 | 0 | 0 | -3 |
| GraphRAG | 0.3421 | 0.7222 | 0.4643 | 50 | 10 | 15 | 10 | 10 | 5 | 0 |

## SCN-005

**Query:** Does Viktor Kasarov have any links to high-risk or sanctioned entities?

- Winner: `GraphRAG`
- GraphRAG vs LLM-Only deltas: tokens `89.1%`, latency `99.73%`, cost `100.0%`, judge `2000.0%`

| Pipeline | BERT P | BERT R | BERT F1 | Judge Total | Entity | Path | Relation | Traversal | Multi-hop | Hallucination Penalty |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| LLM-Only | 0.0634 | 0.3333 | 0.1065 | 1 | 4 | 2 | 0 | 0 | 1 | -6 |
| Vector-RAG | 0.1538 | 0.3704 | 0.2174 | 7 | 8 | 5 | 0 | 0 | 4 | -10 |
| GraphRAG | 0.2500 | 0.2222 | 0.2353 | 21 | 6 | 5 | 10 | 0 | 3 | -3 |

## Pipeline Averages (Across All Scenarios)

| Pipeline | Avg BERT P | Avg BERT R | Avg BERT F1 | Avg Judge Total | Avg Entity | Avg Path | Avg Relation | Avg Traversal | Avg Multi-hop | Avg Hallucination Penalty |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| LLM-Only | 0.0463 | 0.3617 | 0.0815 | 2.2000 | 4.8000 | 2.4000 | 1.0000 | 1.2000 | 1.4000 | -9.0000 |
| Vector-RAG | 0.0805 | 0.1804 | 0.1101 | 2.6000 | 4.4000 | 1.8000 | 0.6000 | 0.0000 | 1.6000 | -6.8000 |
| GraphRAG | 0.2186 | 0.3908 | 0.2707 | 26.6000 | 7.6000 | 9.0000 | 5.8000 | 5.0000 | 3.6000 | -4.4000 |
