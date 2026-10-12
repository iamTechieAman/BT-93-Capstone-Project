// ============================================================================
// Neo4j Cypher Reasoning Queries for Smart GST System
// Demonstrates multi-hop reasoning, hierarchy traversal, rule traversal, and provenance.
// ============================================================================

// 1. Full Multi-Hop Reasoning Path Query
// Product -> Material -> Category -> HSN -> GST Rule -> GST Rate -> Source
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

// 2. HSN Hierarchy Traversal Query
// HSN Code -> Heading -> Chapter
MATCH (hc:HsnCode {code: "42031010"})
      -[r1:SUB_HEADING_OF]-> (h:HsnHeading)
      -[r2:CHAPTER_OF]-> (ch:HsnChapter)
RETURN hc.code AS HSN_Code,
       hc.technical_description AS HSN_Description,
       h.heading_code AS Heading_Code,
       h.description AS Heading_Description,
       ch.chapter_code AS Chapter_Code,
       ch.title AS Chapter_Title,
       r1.evidence_source AS Subheading_Evidence,
       r2.evidence_source AS Chapter_Evidence;

// 3. GST Rule & Rate Traversal Query
// HSN Code -> GST Rule -> Rates & Conditions
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

// 4. Source Provenance Traversal Query
// Find all HSN Codes & Rules backed by a specific CBIC Notification
MATCH (src:SourceDocument {notification_number: "1/2017-Central Tax (Rate)"})
      <-[r:EVIDENCED_BY]- (n)
RETURN src.notification_number AS Notification,
       src.title AS Document_Title,
       labels(n)[0] AS Entity_Type,
       COALESCE(n.code, n.rule_id, n.product_id) AS Entity_ID,
       r.evidence_source AS Evidence_Citation;
