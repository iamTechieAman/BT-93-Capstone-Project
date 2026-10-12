# Smart GST Knowledge Graph — Cypher Query Reference Manual

## 1. Multi-Hop Reasoning Path Query

Traces the complete 7-hop reasoning path from a product submission back to authoritative CBIC source document provenance:

```cypher
MATCH (p:Product {name: $product_name})
      -[r1:PRODUCT_HAS_ATTRIBUTE]->(m:Material)
      -[r2:PRODUCT_CANDIDATE_HSN]->(h:HSN)
      -[r3:HSN_GOVERNED_BY]->(gr:GST_Rule)
      -[r4:HSN_TAXED_AT]->(rate:GST_Rate)
      -[r5:RULE_DEFINED_IN]->(n:Notification)
      -[:SOURCE_SUPPORTS_RULE]-(src:Source)
RETURN p.name AS Product,
       m.name AS Material,
       h.code AS HsnCode,
       gr.rule_name AS Rule,
       rate.gst_rate AS TaxRate,
       n.notification_number AS Notification,
       src.document_url AS SourceURL,
       r3.evidence_source AS EvidenceCitation;
```

---

## 2. Tariff Hierarchy Traversal Query

Traverses the 8-digit HSN  6-digit Subheading  4-digit Heading  2-digit Chapter taxonomy:

```cypher
MATCH (h:HSN {code: $hsn_code})
      -[:HSN_CHILD_OF]->(sub:Subheading)
      -[:HSN_CHILD_OF]->(hd:Heading)
      -[:HSN_BELONGS_TO_CHAPTER]->(ch:Chapter)
RETURN h.code AS HsnCode,
       h.technical_description AS HsnDescription,
       hd.heading_code AS HeadingCode,
       hd.description AS HeadingDescription,
       ch.chapter_code AS ChapterCode,
       ch.title AS ChapterTitle;
```

---

## 3. Conflict Detection Query

Identifies HSN or SAC codes assigned conflicting active tax rates:

```cypher
MATCH (h:HSN)-[:HSN_TAXED_AT]->(r1:GST_Rate),
      (h:HSN)-[:HSN_TAXED_AT]->(r2:GST_Rate)
WHERE r1.rate_id <> r2.rate_id AND r1.gst_rate <> r2.gst_rate
RETURN h.code AS HsnCode,
       r1.gst_rate AS Rate1,
       r2.gst_rate AS Rate2,
       "CONFLICTING_TAX_RATES" AS Issue;
```

---

## 4. Expired / Stale Rule Detection Query

Identifies tax rules whose parent notification `effective_to` date has passed:

```cypher
MATCH (gr:GST_Rule)-[:RULE_DEFINED_IN]->(n:Notification)
WHERE n.effective_to IS NOT NULL AND date(n.effective_to) < date()
RETURN gr.rule_id AS RuleID,
       gr.rule_name AS RuleName,
       n.notification_number AS NotificationNumber,
       n.effective_to AS ExpiryDate,
       "STALE_EXPIRED_RULE" AS Issue;
```

---

## 5. Orphan Node Detection Query

Identifies isolated graph nodes that lack relationship edges:

```cypher
MATCH (n)
WHERE NOT (n)-[]-()
RETURN labels(n) AS NodeLabel,
       properties(n) AS NodeProperties,
       "ORPHAN_NODE" AS Issue;
```
