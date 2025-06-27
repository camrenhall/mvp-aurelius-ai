# MVP Document-Automation Platform

*(Lightweight Architecture Overview • v0.1)*

---

## 1 · Purpose

Build a **two-vertical MVP** (Family-Law discovery & Corporate-Real-Estate lease abstraction) that:

1. **Ingests** any incoming legal PDF/scan.
2. **Extracts** key fields into structured JSON.
3. **Validates** completeness and basic business rules.
4. **Surfaces** low-confidence items for human review.
5. **Exports** data to Excel/CSV or downstream APIs.

Target timeline: **≈ 3 weeks** to first live demo, without locking the product into any single vendor or model.

---

## 2 · Guiding Principles

| Principle                                 | Why it Matters                                                                                                                   |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **Start production-quality, then refine** | Shipping partial features on robust patterns avoids rewrites.                                                                    |
| **Pluggable engines**                     | OCR & extraction sit behind thin adapters—swap Textract ↔ self-host OCR, or OpenAI ↔ fine-tuned LayoutLM with one config change. |
| **Data residency first**                  | Raw documents remain in your cloud account (S3 + KMS). External LLMs only receive redacted text blocks.                          |
| **Single-source schema**                  | JSON schemas (one per vertical) drive extraction, validation, and UI—change a field once, everywhere updates.                    |
| **Human-in-loop by design**               | Confidence scoring + review UI ensures early accuracy and creates labelled data for future training.                             |

---

## 3 · High-Level Architecture

```text
Client Upload  →  Ingest API  ─┐
                               ▼
                    ①  OCR & Layout Service
                        • MVP: AWS Textract “Queries”
                        • Upgrade: Azure DI container / Tesseract+LayoutLM

                               ▼
                    ②  Extraction Orchestrator (LangChain)
                        • Primary: OpenAI o3/4o function-calling
                        • Optional ensemble: regex heuristics, future LayoutLMv3

                               ▼
                    ③  Validation Engine
                        • Pydantic rules + schema completeness
                        • Cross-field logic (e.g., Start ≤ End dates)

                               ▼
                    ④  Persistence
                        • Postgres (metadata & extracted JSON)
                        • S3 (raw & OCR outputs)
                        • Versioned audit log (immutable append)

                               ▼
                    ⑤  Review / Export
                        • Next.js UI: status board, side-by-side viewer
                        • One-click Excel / CSV
                        • Webhooks for downstream systems
```

> **Latency target:** < 60 s from upload to reviewer queue for a 10-page PDF.

---

## 4 · Core Components

| # | Component                | Responsibilities                                      | Quick-Start Choice                               |
| - | ------------------------ | ----------------------------------------------------- | ------------------------------------------------ |
| ① | **Ingest Service**       | Presigned-URL upload, S3 storage, EventBridge trigger | AWS Lambda + Python                              |
| ② | **OCR / Layout**         | Turn scans into text + bounding boxes                 | Textract “DocumentTextDetection” & “Queries”     |
| ③ | **Extraction Layer**     | Populate schema via LLM function calling              | openai-python + LangChain                        |
| ④ | **Validation Layer**     | Confidence thresholds, rule checks, status flags      | Pydantic models                                  |
| ⑤ | **Review UI**            | List matters, show discrepancies, approve / edit      | Next.js + Supabase auth                          |
| ⑥ | **Export / Integration** | Excel/CSV template matching current workflows         | Pandas → `to_excel()` download; webhook skeleton |

---

## 5 · Security & Compliance

* **Data at Rest:** S3 SSE-KMS + Postgres AES-256.
* **Data in Transit:** TLS 1.3 everywhere.
* **PII Boundary:** Only OCR-extracted text sent to OpenAI; raw docs never leave VPC.
* **Audit Trail:** SHA-256 hash of every upload; immutable log table with user, timestamp, diff.
* **Auth:** Magic-link + RBAC (viewer, reviewer, admin).

---

## 6 · MVP Success Criteria

| Metric                               | Threshold              |
| ------------------------------------ | ---------------------- |
| Field recall on synthetic sample set | ≥ 85 %                 |
| Average reviewer correction time     | ≤ 5 min per doc        |
| Upload → reviewable status latency   | ≤ 60 s for 10-page doc |
| Zero critical security findings      | Automated scan passes  |

---

## 7 · Day-0 Setup Checklist

1. **Define JSON schemas** (`family_discovery.json`, `lease_abstraction.json`).
2. **Provision AWS baseline** (S3, EventBridge, Lambda, RDS Free Tier).
3. **Create Git repo + CI/CD pipeline** (GitHub Actions → Terraform).
4. **Collect 10 public sample PDFs per vertical** for smoke tests.
5. **Draft first-pass OpenAI prompts** with 2–3 few-shot examples each.

---

## 8 · Future-Proof Upgrades

* **Accuracy:** Add fine-tuned LayoutLMv3 micro-service; enable model ensemble voting.
* **Performance:** Containerise OCR & extraction; run on GPU spot instances.
* **Integrations:** Push directly to E-Immigration API, SharePoint, or CRE BI dashboards via webhooks.
* **Analytics:** Store embeddings in PGVector for semantic search across matter corpus.

---

**Reference Usage:** Drop this document into any LLM chat or internal repo when discussing scope, architecture, or trade-offs for the MVP.
