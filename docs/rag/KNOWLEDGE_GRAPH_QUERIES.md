# Knowledge Graph Cypher Queries & Traversal Patterns

## 1. Multi-Hop Reasoning Query Path

Traces the complete 7-step path from raw product description to statutory source document citation:
```
Product -> Material -> Category -> HSN Code -> GST Rule -> GST Rate -> Source Document
```

### Cypher Query
```cypher
MATCH path = (p:Product {name: "Leather Jacket with Zip"})
             -[r1:MADE_OF]-> (m:Material)
             -[r2:USED_IN_CATEGORY]-> (c:ItemCategory)
             -[r3:GOVERNS_HSN]-> (hsn:HsnCode)
             -[r4:GOVERNED_BY]-> (rule:GstRule)
             -[r5:HAS_RATE]-> (rate:GstRate)
             -[r6:EVIDENCED_BY]-> (src:SourceDocument)
RETURN p.name AS Product,
       m.name AS Material,
       hsn.code AS HSN,
       hsn.technical_description AS Description,
       rule.rule_name AS Rule,
       rate.gst_rate AS TaxRate,
       src.notification_number AS Citation,
       r6.evidence_source AS Evidence;
```

### Example API Output Response
```json
{
  "product_name": "Leather Jacket with Zip",
  "hsn_code": "42031010",
  "gst_rate": 18.0,
  "source_citation": "1/2017-Central Tax (Rate)",
  "reasoning_chain": [
    {"hop": 1, "step": "Product", "node": "Leather Jacket with Zip"},
    {"hop": 2, "step": "Material", "node": "Bovine Leather", "relationship": "MADE_OF", "evidence": "Product Spec / CBIC Chapter 42 Rule"},
    {"hop": 3, "step": "Category", "node": "Apparel & Accessories", "relationship": "BELONGS_TO", "evidence": "Product Spec / Trade Classification"},
    {"hop": 4, "step": "HSN Code", "node": "42031010", "relationship": "CLASSIFIED_UNDER", "evidence": "Multi-Agent Decision Pipeline & CBIC Entry 112"},
    {"hop": 5, "step": "GST Rule", "node": "Leather Apparel Schedule Rule", "relationship": "GOVERNED_BY", "evidence": "CBIC Notification No. 1/2017-Central Tax (Rate), Entry 112"},
    {"hop": 6, "step": "GST Rate", "node": "18.0% GST", "relationship": "HAS_RATE", "evidence": "CBIC Schedule III Entry 112"},
    {"hop": 7, "step": "Source Provenance", "node": "1/2017-Central Tax (Rate)", "relationship": "EVIDENCED_BY", "evidence": "CBIC Statutory Notification Schedule"}
  ]
}
```

---

## 2. HSN Hierarchy Traversal Query

Traverses the tariff hierarchy: `HSN Code -> Heading -> Chapter`.

### Cypher Query
```cypher
MATCH (hc:HsnCode {code: "42031010"})
      -[r1:SUB_HEADING_OF]-> (h:HsnHeading)
      -[r2:CHAPTER_OF]-> (ch:HsnChapter)
RETURN hc.code AS HSN_Code,
       h.heading_code AS Heading_Code,
       ch.chapter_code AS Chapter_Code,
       ch.title AS Chapter_Title,
       r1.evidence_source AS Subheading_Evidence,
       r2.evidence_source AS Chapter_Evidence;
```

---

## 3. GST Rule & Rate Traversal Query

Traverses governing rules and tax rates: `HSN Code -> GST Rule -> Rates & Conditions`.

### Cypher Query
```cypher
MATCH (hc:HsnCode {code: "42031010"})
      -[r1:GOVERNED_BY]-> (rule:GstRule)
      -[r2:HAS_RATE]-> (rate:GstRate)
RETURN hc.code AS HSN,
       rule.rule_id AS Rule_ID,
       rule.rule_name AS Rule_Name,
       rule.conditions AS Conditions,
       rate.gst_rate AS Total_GST,
       rate.cgst_rate AS CGST,
       rate.sgst_rate AS SGST,
       rate.igst_rate AS IGST,
       r1.evidence_source AS Rule_Evidence;
```

---

## 4. Source Provenance Traversal Query

Traces HSN codes and rules back to statutory CBIC notifications: `HSN Code / Rule -> Source Document`.

### Cypher Query
```cypher
MATCH (src:SourceDocument {notification_number: "1/2017-Central Tax (Rate)"})
      <-[r:EVIDENCED_BY]- (n)
RETURN src.notification_number AS Notification,
       src.title AS Document_Title,
       labels(n)[0] AS Entity_Type,
       COALESCE(n.code, n.rule_id, n.product_id) AS Entity_ID,
       r.evidence_source AS Evidence_Citation;
```
