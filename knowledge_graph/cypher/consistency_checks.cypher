// Knowledge Graph Consistency, Conflict & Orphan Detection Queries

// 1. Conflict Detection: Find HSN/SAC codes mapped to multiple conflicting active GST Rates
MATCH (h:HSN)-[:HSN_TAXED_AT]->(r1:GST_Rate),
      (h:HSN)-[:HSN_TAXED_AT]->(r2:GST_Rate)
WHERE r1.rate_id <> r2.rate_id AND r1.gst_rate <> r2.gst_rate
RETURN h.code AS HsnCode, r1.gst_rate AS Rate1, r2.gst_rate AS Rate2, "CONFLICTING_TAX_RATES" AS ConflictType;

// 2. Stale-Rule Detection: Find GST Rules whose parent Notification has expired (effective_to < current_date)
MATCH (gr:GST_Rule)-[:RULE_DEFINED_IN]->(n:Notification)
WHERE n.effective_to IS NOT NULL AND date(n.effective_to) < date()
RETURN gr.rule_id AS RuleID, gr.rule_name AS RuleName, n.notification_number AS NotificationNumber, n.effective_to AS ExpiredOn, "STALE_RULE" AS IssueType;

// 3. Orphan-Node Detection: Find nodes with 0 relationships
MATCH (n)
WHERE NOT (n)-[]-()
RETURN labels(n) AS NodeLabel, properties(n) AS NodeProperties, "ORPHAN_NODE" AS IssueType;

// 4. Unbacked Rule Detection: Find GST Rules missing an authoritative Source support link
MATCH (gr:GST_Rule)
WHERE NOT (gr)<-[:SOURCE_SUPPORTS_RULE]-(:Source)
RETURN gr.rule_id AS RuleID, gr.rule_name AS RuleName, "MISSING_SOURCE_PROVENANCE" AS IssueType;
