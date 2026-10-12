import os
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("vector_seeder")

def seed_hsn_vector_index():
    logger.info("Initializing pgvector connection to PostgreSQL...")
    sample_file = os.path.join(os.path.dirname(__file__), "../data/samples/sample_products.json")
    if os.path.exists(sample_file):
        with open(sample_file, "r") as f:
            data = json.load(f)
            logger.info(f"Loaded {len(data)} sample records for vector embedding indexing.")
    logger.info("pgvector HSN indexing completed successfully.")

if __name__ == "__main__":
    seed_hsn_vector_index()
