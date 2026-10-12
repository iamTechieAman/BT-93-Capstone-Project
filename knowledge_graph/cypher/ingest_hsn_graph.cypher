// ============================================================================
// Neo4j Cypher Ingestion Script for Smart GST System
// Ingests HSN nodes, GST rules, rates, sources, and evidence relationships.
// "No graph relationship should be created without evidence."
// ============================================================================

// 1. Ingest Source Documents
MERGE (s1:SourceDocument {document_id: "DOC-CBIC-01-2017"})
ON CREATE SET s1.notification_number = "1/2017-Central Tax (Rate)",
              s1.title = "CBIC Notification No. 1/2017-Central Tax (Rate), Schedule III",
              s1.source_url = "https://cbic-gst.gov.in/pdf/Notification1-CGST-Rate.pdf",
              s1.effective_from = "2017-07-01";

MERGE (s2:SourceDocument {document_id: "DOC-CBIC-08-2021"})
ON CREATE SET s2.notification_number = "8/2021-Central Tax (Rate)",
              s2.title = "CBIC Notification No. 8/2021-Central Tax (Rate)",
              s2.source_url = "https://cbic-gst.gov.in/pdf/Notification8-CGST-Rate.pdf",
              s2.effective_from = "2021-10-01";

MERGE (s3:SourceDocument {document_id: "DOC-CBIC-02-2017"})
ON CREATE SET s3.notification_number = "2/2017-Central Tax (Rate)",
              s3.title = "CBIC Notification No. 2/2017-Central Tax (Rate), Schedule Nil",
              s3.source_url = "https://cbic-gst.gov.in/pdf/Notification2-CGST-Rate.pdf",
              s3.effective_from = "2017-07-01";

// 2. Ingest Chapters & Headings
MERGE (ch42:HsnChapter {chapter_code: "42"})
ON CREATE SET ch42.title = "Articles of leather; saddlery and harness; travel goods, handbags";

MERGE (h4203:HsnHeading {heading_code: "4203"})
ON CREATE SET h4203.description = "Articles of apparel and clothing accessories, of leather or of composition leather";

MERGE (h4203)-[r_ch1:CHAPTER_OF {evidence_source: "CBIC Tariff Schedule 2017", validation_status: "VERIFIED_AUTHORITATIVE"}]->(ch42);

// 3. Ingest HSN Code & Rule
MERGE (hc4203:HsnCode {code: "42031010"})
ON CREATE SET hc4203.technical_description = "Articles of apparel and clothing accessories, of leather or of composition leather - Jackets and blazers",
              hc4203.trade_description = "Leather biker jacket";

MERGE (hc4203)-[r_sub1:SUB_HEADING_OF {evidence_source: "CBIC Tariff Schedule 2017", validation_status: "VERIFIED_AUTHORITATIVE"}]->(h4203);
MERGE (hc4203)-[r_ev1:EVIDENCED_BY {evidence_source: "CBIC Notification No. 1/2017-Central Tax (Rate)", validation_status: "VERIFIED_AUTHORITATIVE"}]->(s1);

MERGE (rule4203:GstRule {rule_id: "RULE-4203-APP-18"})
ON CREATE SET rule4203.rule_name = "Leather Apparel Schedule Rule",
              rule4203.conditions = "Standard apparel schedule rate. Excludes articles of fur.",
              rule4203.exceptions = "Heading 4303 fur apparel excluded";

MERGE (rate18:GstRate {rate_id: "RATE-18-SCHED-3"})
ON CREATE SET rate18.gst_rate = 18.0, rate18.cgst_rate = 9.0, rate18.sgst_rate = 9.0, rate18.igst_rate = 18.0, rate18.cess_rate = 0.0;

MERGE (hc4203)-[r_gov1:GOVERNED_BY {evidence_source: "CBIC Notification No. 1/2017-Central Tax (Rate), Entry 112", validation_status: "VERIFIED_AUTHORITATIVE"}]->(rule4203);
MERGE (rule4203)-[r_rate1:HAS_RATE {evidence_source: "CBIC Schedule III Entry 112", validation_status: "VERIFIED_AUTHORITATIVE"}]->(rate18);
MERGE (rule4203)-[r_src1:EVIDENCED_BY {evidence_source: "CBIC Notification No. 1/2017-Central Tax (Rate)", validation_status: "VERIFIED_AUTHORITATIVE"}]->(s1);

// 4. Ingest Sample Product & Attributes with Evidence Links
MERGE (prod1:Product {product_id: "PROD-LEATHER-JACKET-01"})
ON CREATE SET prod1.name = "Leather Jacket with Zip",
              prod1.description = "Men's biker style genuine leather jacket with metallic zipper";

MERGE (matLeather:Material {material_id: "MAT-LEATHER"})
ON CREATE SET matLeather.name = "Bovine Leather";

MERGE (catApparel:ItemCategory {category_id: "CAT-APPAREL"})
ON CREATE SET catApparel.name = "Apparel & Accessories";

MERGE (prod1)-[r_m1:MADE_OF {evidence_source: "Product Spec / CBIC Chapter 42 Rule", validation_status: "VERIFIED_AUTHORITATIVE", confidence: 0.98}]->(matLeather);
MERGE (prod1)-[r_b1:BELONGS_TO {evidence_source: "Product Spec / Trade Classification", validation_status: "VERIFIED_AUTHORITATIVE"}]->(catApparel);
MERGE (prod1)-[r_c1:CLASSIFIED_UNDER {evidence_source: "Multi-Agent Decision Pipeline & CBIC Entry 112", validation_status: "VERIFIED_AUTHORITATIVE", confidence: 0.96}]->(hc4203);
