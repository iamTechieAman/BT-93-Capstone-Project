# System Use Cases Specification

## Use Case Catalog

| Use Case ID | Use Case Name | Primary Actor | Description | Preconditions |
| :--- | :--- | :--- | :--- | :--- |
| **UC-001** | Verify Product GST & HSN | `USER` | User enters trade description to execute multi-agent classification, evidence retrieval, and rate verification. | User accesses AI Studio tab. |
| **UC-002** | Generate Sales Tax Invoice | `USER` | User adds verified products to sales transaction, selects supply state, and issues Rule 46 compliant tax invoice. | Line items verified or entered. |
| **UC-003** | Inspect Audit Trail | `COMPLIANCE_OFFICER` | Compliance officer views immutable verification logs and exports audit JSON. | Authenticated user access. |
| **UC-004** | Manage Authoritative GST Rules | `ADMIN` | Admin updates canonical HSN codes, statutory GST rate rules, or CBIC source documents. | Authenticated with `ADMIN` or `COMPLIANCE_OFFICER` role. |
| **UC-005** | Trigger Knowledge Graph Sync | `ADMIN` | Admin triggers re-synchronization of Neo4j Knowledge Graph ontology nodes and edges. | Authenticated with `ADMIN` role. |

---

## Detailed Use Case Specification: UC-001 (Verify Product GST & HSN)

- **Primary Actor**: `USER`
- **Preconditions**: Web client active at `http://localhost:5173`.
- **Main Success Scenario**:
  1. User enters natural-language description (e.g. *"Biker style genuine leather jacket with zipper"*).
  2. User selects intra-state or inter-state supply type and clicks "Verify GST".
  3. System normalizes text, executes hybrid vector search (pgvector), queries Neo4j graph, fetches RAG chunks, and invokes Gemini AI decision engine.
  4. System deterministically reconciles LLM output against PostgreSQL GST rule database.
  5. UI renders suggested HSN `42031010`, GST rate `18%`, confidence score `96%`, evidence citations, and Evidence-Backed Explanation.
- **Extensions / Error Scenarios**:
  - *Input Empty*: System displays `AlertCircle` warning ("Please enter a valid product description").
  - *Ambiguous Candidate*: System flags `classification_status: AMBIGUOUS` and prompts clarifying questions.
