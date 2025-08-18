import os
import pandas as pd
from sqlalchemy.engine import Engine
from db import get_engine

# --- File Paths ---
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SRC_DIR)
SQL_FILE_PATH = os.path.join(PROJECT_ROOT, 'sql', 'queries.sql')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'data')


def read_and_split_queries(file_path: str) -> list[str]:
    """
    Reads a .sql file and splits it into a list of individual queries.
    Assumes queries are separated by semicolons ';'.
    """
    print(f"Reading queries from {file_path}...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        queries = [q.strip() for q in content.split(';') if q.strip()]

        return queries
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return []


def execute_transformations():
    """
    Main function to execute SQL transformations and save results to CSV.
    """
    print("--- Starting Transformation Step ---")
    
    engine = get_engine()
    queries = read_and_split_queries(SQL_FILE_PATH)
    
    output_filenames = [
        "query_1_max_coffee_value_day.csv",
        "query_2_annual_summary.csv",
        "query_3_monthly_annual_averages.csv"
    ]

    if len(queries) != len(output_filenames):
        print("Error: The number of queries does not match the number of output filenames.")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for i, query in enumerate(queries):
        query_num = i + 1
        output_file = output_filenames[i]
        output_path = os.path.join(OUTPUT_DIR, output_file)

        print(f"\nExecuting Query {query_num}...")
        try:
            df = pd.read_sql_query(query, engine)
            df.to_csv(output_path, index=False)
            print(f"Success! Results for Query {query_num} saved to '{output_path}'")
            print("--- Result Preview ---")
            print(df.head())
            
        except Exception as e:
            print(f"Error executing Query {query_num}: {e}")

    print("\n--- Transformation Step Finished ---")


if __name__ == "__main__":
    execute_transformations()