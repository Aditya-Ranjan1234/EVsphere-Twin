import os
import csv
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

# Neo4j connection – reads from .env if present, otherwise defaults to local container
NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', '')  # empty for local dev (no auth)

def get_driver():
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def ingest_csv_folder(folder_path: str, node_label: str = "Entity"):
    """Ingest all CSV files in *folder_path* into Neo4j.
    Each CSV is expected to have at least the columns ``source`` and ``target``.
    Optional ``type`` column becomes the relationship type (defaults to ``RELATED``).
    """
    driver = get_driver()
    with driver.session() as session:
        for filename in os.listdir(folder_path):
            if not filename.lower().endswith('.csv'):
                continue
            csv_path = os.path.join(folder_path, filename)
            with open(csv_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    src = row.get('source') or row.get('Source')
                    tgt = row.get('target') or row.get('Target')
                    rel_type = (row.get('type') or row.get('Type') or 'RELATED').upper()
                    if not src or not tgt:
                        continue
                    # Merge nodes and relationship
                    session.run(
                        f"MERGE (a:{node_label} {{id: $src}}) "
                        f"MERGE (b:{node_label} {{id: $tgt}}) "
                        f"MERGE (a)-[r:{rel_type}]->(b)",
                        src=src, tgt=tgt)
    driver.close()

if __name__ == "__main__":
    data_dir = os.getenv('DATA_DIR', os.path.abspath('data'))
    ingest_csv_folder(data_dir)
