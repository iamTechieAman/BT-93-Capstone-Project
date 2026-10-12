// Seed Cypher script for Neo4j

CREATE (c42:Chapter {code: "42", description: "Articles of leather; saddlery and harness"})
CREATE (h4203:Heading {code: "4203", description: "Articles of apparel and clothing accessories, of leather or of composition leather"})
CREATE (r18:GST_Rate {rate: 18.0, name: "Standard 18%"})
CREATE (n1:Notification {number: "Notification No. 1/2017-CT", schedule: "Schedule III, S.No. 111"})

CREATE (h4203)-[:BELONGS_TO_CHAPTER]->(c42)
CREATE (h4203)-[:TAXED_AT]->(r18)
CREATE (h4203)-[:GOVERNED_BY]->(n1)

CREATE (mLeather:Material {name: "Leather / Composition Leather"})
CREATE (pJacket:Product {name: "Leather Jacket with Zip"})

CREATE (pJacket)-[:MADE_OF]->(mLeather)
CREATE (mLeather)-[:CLASSIFIED_UNDER]->(h4203);
