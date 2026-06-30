import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

POSTGRES_URL = os.getenv('POSTGRES_URL')

def get_engine():
    return create_engine(POSTGRES_URL)

def ingest_csv(csv_path: str, table_name: str, if_exists: str = 'replace'):
    """Read a CSV file and load it into PostgreSQL.
    Args:
        csv_path: Path to the CSV file.
        table_name: Destination table name.
        if_exists: Behavior if table exists ('replace' or 'append').
    """
    df = pd.read_csv(csv_path)
    engine = get_engine()
    df.to_sql(table_name, con=engine, if_exists=if_exists, index=False)
    print(f"Loaded {len(df)} rows into {table_name}")

if __name__ == "__main__":
    # Example usage: python data_ingest.py data/supplier.csv supplier_table
    import sys
    if len(sys.argv) != 3:
        print("Usage: python data_ingest.py <csv_path> <table_name>")
    else:
        ingest_csv(sys.argv[1], sys.argv[2])
