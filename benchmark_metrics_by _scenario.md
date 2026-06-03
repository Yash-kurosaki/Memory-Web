# Benchmark Metrics by Scenario — All 30 Scenarios

> **Generated:** 2026-05-31T10:09:26.748305+00:00  
> **Dataset:** 913,931,776 tokens  
> **Source of truth:** `benchmark_report.json` (latest post-Savanna run)

## Results Table

| Scenario | Query | Winner | GraphRAG Tokens | Basic RAG Tokens | Token Reduction | Judge | BERTScore F1 | Latency | Cost |
|----------|-------|--------|---------------:|----------------:|----------------:|-------|:------------:|---------|------|
| SCN-001 | Who is the ultimate beneficial owner of Meridian Holdings Lt… | **LLM-Only** | 576 | 1,638 | 64.8% | ✅ PASS | 0.8800 | 1.92s | $0.000053 |
| SCN-002 | Does Vertex Capital have any indirect exposure to sanctioned… | **LLM-Only** | 616 | 1,629 | 62.2% | ✅ PASS | 0.8750 | 3.14s | $0.000052 |
| SCN-003 | What links Horizon Group to sanctioned activities? | **LLM-Only** | 563 | 1,667 | 66.2% | ✅ PASS | 0.7943 | 1.95s | $0.000057 |
| SCN-004 | What is the shortest exposure chain between Jonathan Doe and… | **GraphRAG** | 276 | 1,687 | 83.6% | ✅ PASS | 0.9700 | 1.63s | $0.000034 |
| SCN-005 | Who are the real beneficiaries behind the Cayman Islands tru… | **GraphRAG** | 330 | 1,675 | 80.3% | ❌ FAIL | 0.9229 | 1.91s | $0.000049 |
| SCN-006 | Map all entities within 2 degrees of separation from the san… | **GraphRAG** | 538 | 1,677 | 67.9% | ✅ PASS | 0.9700 | 2.34s | $0.000087 |
| SCN-007 | Does Helios Maritime connect to any politically exposed pers… | **GraphRAG** | 228 | 1,685 | 86.5% | ✅ PASS | 0.8445 | 1.71s | $0.000026 |
| SCN-008 | Is there a circular ownership loop involving Orion Ventures? | **GraphRAG** | 217 | 1,636 | 86.7% | ✅ PASS | 0.9463 | 1.32s | $0.000026 |
| SCN-009 | Trace the transaction flow from Baltic Import Ltd to any san… | **GraphRAG** | 252 | 1,671 | 84.9% | ✅ PASS | 0.9656 | 1.27s | $0.000031 |
| SCN-010 | Identify the ultimate controlling person behind Northbridge … | **GraphRAG** | 256 | 1,623 | 84.2% | ✅ PASS | 0.9423 | 1.44s | $0.000031 |
| SCN-011 | Which companies share bank account BA-77192 with Emerald Gat… | **GraphRAG** | 212 | 1,657 | 87.2% | ✅ PASS | 0.8333 | 1.67s | $0.000023 |
| SCN-012 | Show all shell companies registered by Blue Reef Corporate S… | **GraphRAG** | 270 | 1,659 | 83.7% | ✅ PASS | 0.8651 | 1.87s | $0.000030 |
| SCN-013 | Do Luma Capital and Granite Freight have overlapping directo… | **LLM-Only** | 266 | 1,647 | 83.8% | ✅ PASS | 0.8467 | 1.71s | $0.000034 |
| SCN-014 | Find the highest-risk cluster of entities sharing 88 Coral S… | **GraphRAG** | 182 | 1,669 | 89.1% | ❌ FAIL | 0.7000 | 1.48s | $0.000018 |
| SCN-015 | What is the cross-border chain from Lotus Finance to the san… | **GraphRAG** | 267 | 1,705 | 84.3% | ✅ PASS | 0.9700 | 1.84s | $0.000031 |
| SCN-016 | Is Atlas Medical Supplies ultimately controlled by any sanct… | **GraphRAG** | 266 | 1,642 | 83.8% | ✅ PASS | 0.8909 | 1.52s | $0.000034 |
| SCN-017 | Which entities are central in rapid pass-through transfers l… | **GraphRAG** | 232 | 1,639 | 85.8% | ✅ PASS | 0.9333 | 1.56s | $0.000027 |
| SCN-018 | Does Meridian Health Ventures have indirect exposure to any … | **GraphRAG** | 233 | 1,677 | 86.1% | ✅ PASS | 0.9208 | 1.46s | $0.000028 |
| SCN-019 | Detect the layering pattern connecting Pinebridge Traders to… | **GraphRAG** | 266 | 1,655 | 83.9% | ✅ PASS | 0.8783 | 1.68s | $0.000033 |
| SCN-020 | How many shell layers exist between Crescent Bio Ltd and its… | **GraphRAG** | 267 | 1,669 | 84.0% | ✅ PASS | 0.8451 | 1.66s | $0.000034 |
| SCN-021 | Which entities share the same sanctioned counterparty as Alt… | **GraphRAG** | 198 | 1,655 | 88.0% | ✅ PASS | 0.8800 | 1.48s | $0.000021 |
| SCN-022 | Trace any influence chain from PEP Natalia Sokolova to Westb… | **GraphRAG** | 230 | 1,668 | 86.2% | ✅ PASS | 0.9510 | 1.29s | $0.000026 |
| SCN-023 | How does sanctions risk propagate from Arctic Minerals PLC t… | **GraphRAG** | 213 | 1,041 | 79.5% | ✅ PASS | 0.8388 | 1.54s | $0.000024 |
| SCN-024 | Are there board interlocks between sanctioned firms and Nova… | **GraphRAG** | 193 | 1,684 | 88.5% | ✅ PASS | 0.8800 | 1.72s | $0.000020 |
| SCN-025 | Is the connection between Crownline Energy and Red Banner Me… | **GraphRAG** | 222 | 1,668 | 86.7% | ✅ PASS | 0.9700 | 1.34s | $0.000025 |
| SCN-026 | Which offshore jurisdictions appear in the chain behind Beac… | **GraphRAG** | 283 | 1,650 | 82.8% | ✅ PASS | 0.7364 | 1.83s | $0.000037 |
| SCN-027 | Does Summit Advisory Group have multiple final beneficiaries… | **GraphRAG** | 225 | 1,632 | 86.2% | ✅ PASS | 0.9061 | 1.10s | $0.000027 |
| SCN-028 | Find any laundering path involving correspondent banks betwe… | **GraphRAG** | 252 | 1,668 | 84.9% | ✅ PASS | 0.8757 | 1.33s | $0.000031 |
| SCN-029 | Which single entity acts as the bridge between Sunrise Commo… | **GraphRAG** | 258 | 1,628 | 84.2% | ✅ PASS | 0.9019 | 1.27s | $0.000032 |
| SCN-030 | Who ultimately controls the entities in the Lagoon Ventures … | **GraphRAG** | 197 | 1,639 | 88.0% | ✅ PASS | 0.8140 | 1.20s | $0.000021 |

---

## 🏆 Overall Leaderboard (30 Scenarios)

| Pipeline | Wins | Win Rate |
|----------|-----:|---------:|
| **GraphRAG** | 26 | 86.7% |
| **LLM-Only** | 4 | 13.3% |
| **Basic RAG** | 0 | 0.0% |

---

## 📊 Aggregate Statistics

| Metric | Value |
|--------|-------|
| Avg Token Reduction vs Basic RAG | **82.5%** |
| LLM Judge Pass Rate | **9330.0%** |
| Avg BERTScore F1 | **0.8849** |
| Bonus Judge Achieved (≥0.5) | ✅ Yes |
| Bonus BERTScore Achieved (≥0.5) | ✅ Yes |
| Dataset Tokens | 913,931,776 |
| Scenarios Tested | 30 |