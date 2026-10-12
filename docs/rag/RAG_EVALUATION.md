# RAG Retrieval Evaluation & Benchmark Report

## 1. Overview

The RAG Retrieval Evaluator ([`backend/app/rag/rag_evaluator.py`](backend/app/rag/rag_evaluator.py)) measures information retrieval efficiency across a suite of statutory CBIC tax queries.

---

## 2. Evaluation Metrics Definitions

### 1. Recall@K
$$\text{Recall@K} = \frac{|\text{Retrieved Documents in Top K} \cap \text{Relevant Documents}|}{|\text{Relevant Documents}|}$$
Measures the percentage of relevant statutory documents successfully retrieved within the top $K$ positions.

### 2. Precision@K
$$\text{Precision@K} = \frac{|\text{Retrieved Documents in Top K} \cap \text{Relevant Documents}|}{K}$$
Measures the proportion of retrieved chunks in the top $K$ that are genuinely relevant.

### 3. Mean Reciprocal Rank (MRR)
$$\text{MRR} = \frac{1}{|Q|} \sum_{i=1}^{|Q|} \frac{1}{\text{rank}_i}$$
Evaluates how quickly the first relevant statutory document appears in search results.

### 4. Retrieval Latency (ms)
$$\text{Latency} = t_{\text{completed}} - t_{\text{initiated}}$$
Measures total query processing, hybrid scoring, and reranking duration in milliseconds.

---

## 3. Evaluation Benchmark Results

```
=====================================================================================
          SMART GST VERIFIER — RAG PIPELINE EVALUATION BENCHMARK          
=====================================================================================
Total Test Queries          : 5
Mean Retrieval Latency      : 0.34 ms
Mean Reciprocal Rank (MRR)  : 1.0000
Recall@1                    : 100.0%
Recall@3                    : 100.0%
Recall@5                    : 100.0%
Precision@1                 : 100.0%
Precision@3                 : 60.0%
Precision@5                 : 57.33%
=====================================================================================
```

### Detailed Query Breakdown Table

| Query ID | Statutory Query | Expected Document | Top Retrieved Document | Rank | Latency | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RAG-TC01** | Leather apparel GST rate notification and rules | `CBIC-NOTIF-01-2017-SCHED3` | `CBIC-NOTIF-01-2017-SCHED3` | 1 | 0.54 ms |  PASSED |
| **RAG-TC02** | Solar PV module photosensitive semiconductor rate | `CBIC-NOTIF-08-2021-SOLAR` | `CBIC-NOTIF-08-2021-SOLAR` | 1 | 0.30 ms |  PASSED |
| **RAG-TC03** | Unroasted green coffee beans raw nil rate | `CBIC-NOTIF-02-2017-EXEMPT` | `CBIC-NOTIF-02-2017-EXEMPT` | 1 | 0.29 ms |  PASSED |
| **RAG-TC04** | Cotton t-shirt knitted singlet schedule rate | `CBIC-NOTIF-01-2017-SCHED3` | `CBIC-NOTIF-01-2017-SCHED3` | 1 | 0.28 ms |  PASSED |
| **RAG-TC05** | Leather handbag outer surface leather 18% rate | `CBIC-NOTIF-01-2017-SCHED3` | `CBIC-NOTIF-01-2017-SCHED3` | 1 | 0.28 ms |  PASSED |

---

## 4. How to Run Evaluation

Run the CLI benchmark script:
```bash
PYTHONPATH=backend python3 backend/scripts/evaluate_rag.py
```

Run pytest test suite:
```bash
PYTHONPATH=backend python3 -m pytest backend/tests/test_rag_pipeline.py
```
