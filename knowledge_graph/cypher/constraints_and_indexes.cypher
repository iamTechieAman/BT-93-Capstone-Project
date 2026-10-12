// Neo4j Database Constraints & Indexes for Smart GST System Knowledge Graph

// Node Uniqueness Constraints
CREATE CONSTRAINT c_product_id IF NOT EXISTS FOR (p:Product) REQUIRE p.product_id IS UNIQUE;
CREATE CONSTRAINT c_hsn_code IF NOT EXISTS FOR (h:HSN) REQUIRE h.code IS UNIQUE;
CREATE CONSTRAINT c_sac_code IF NOT EXISTS FOR (s:SAC) REQUIRE s.code IS UNIQUE;
CREATE CONSTRAINT c_chapter_code IF NOT EXISTS FOR (ch:Chapter) REQUIRE ch.chapter_code IS UNIQUE;
CREATE CONSTRAINT c_heading_code IF NOT EXISTS FOR (hd:Heading) REQUIRE hd.heading_code IS UNIQUE;
CREATE CONSTRAINT c_subheading_code IF NOT EXISTS FOR (sub:Subheading) REQUIRE sub.subheading_code IS UNIQUE;
CREATE CONSTRAINT c_material_id IF NOT EXISTS FOR (m:Material) REQUIRE m.material_id IS UNIQUE;
CREATE CONSTRAINT c_category_id IF NOT EXISTS FOR (cat:Category) REQUIRE cat.category_id IS UNIQUE;
CREATE CONSTRAINT c_rate_id IF NOT EXISTS FOR (r:GST_Rate) REQUIRE r.rate_id IS UNIQUE;
CREATE CONSTRAINT c_rule_id IF NOT EXISTS FOR (gr:GST_Rule) REQUIRE gr.rule_id IS UNIQUE;
CREATE CONSTRAINT c_notif_id IF NOT EXISTS FOR (n:Notification) REQUIRE n.notification_id IS UNIQUE;
CREATE CONSTRAINT c_condition_id IF NOT EXISTS FOR (c:Condition) REQUIRE c.condition_id IS UNIQUE;
CREATE CONSTRAINT c_source_id IF NOT EXISTS FOR (src:Source) REQUIRE src.source_id IS UNIQUE;

// Performance B-Tree Indexes
CREATE INDEX idx_hsn_code IF NOT EXISTS FOR (h:HSN) ON (h.code);
CREATE INDEX idx_sac_code IF NOT EXISTS FOR (s:SAC) ON (s.code);
CREATE INDEX idx_notif_num IF NOT EXISTS FOR (n:Notification) ON (n.notification_number);
CREATE INDEX idx_material_name IF NOT EXISTS FOR (m:Material) ON (m.name);
CREATE INDEX idx_category_name IF NOT EXISTS FOR (cat:Category) ON (cat.name);
