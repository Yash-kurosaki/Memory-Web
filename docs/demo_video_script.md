# Round 2 Demo Video Script (5-7 min)

00:00 - Intro: We won Round 1 with financial crime domain and scaled Round 2 to 913M tokens.
00:30 - Dataset: SEC EDGAR + Wikipedia corpus and Gemini `count_tokens` proof.
01:30 - Live dashboard query: "Who owns the ultimate parent of Meridian Holdings?"
02:00 - Show all three pipelines running side-by-side.
03:00 - Token comparison (from live benchmark):
  LLM-Only: 324 tokens avg (no retrieval, no context)
  Basic RAG: 5,649 tokens avg (10 real corpus chunks × ~400 words each)
  GraphRAG: 360 tokens avg (3-hop graph path + entity list)

  "GraphRAG uses 93.5% fewer tokens than Basic RAG."
03:30 - Show savings at scale:
  "At 10,000 queries/day: Basic RAG costs $4.31/day.
   GraphRAG costs $0.58/day. That's $1,369 saved per year per system."
04:00 - Accuracy panel:
  "LLM Judge: 100.0% pass rate — bonus threshold achieved."
  "BERTScore F1: 0.9018 — bonus threshold achieved."
  "Both bonuses hit simultaneously."
04:30 - Show graph visualization and 3-hop traversal path.
05:00 - Open full 30-scenario benchmark table.
06:00 - Explain why graph traversal beats vector-only retrieval for AML.
06:30 - Close with results and submission links.
