// Cypher query template to validate entity-HSN-tax relationships

MATCH (p:Product {name: $product_name})-[r1:MADE_OF]->(m:Material)
MATCH (m)-[r2:CLASSIFIED_UNDER]->(h:Heading {code: $hsn_code})
MATCH (h)-[r3:TAXED_AT]->(t:GST_Rate)
MATCH (h)-[r4:GOVERNED_BY]->(n:Notification)
RETURN p.name AS Product, m.name AS Material, h.code AS HSN_Code, t.rate AS GST_Rate, n.number AS Notification;
