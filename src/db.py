import os
import sqlalchemy
from sqlalchemy import create_engine

# --- Build Robust File Paths ---
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SRC_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
DB_PATH = os.path.join(DATA_DIR, 'coffee_rates.db')

DB_URL = f"sqlite:///{DB_PATH}"

def get_engine() -> sqlalchemy.engine.Engine:
    """
    Creates and returns a SQLAlchemy engine connected to the SQLite database.
    It also ensures the data directory exists before creating the engine.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"Database will be created at: {DB_PATH}")
    return create_engine(DB_URL)

def create_database_and_tables(engine: sqlalchemy.engine.Engine):
    """
    Reads the DDL script, splits it into individual statements,
    and executes them one by one to create the database and tables.
    """
    print("Creating database and tables if they don't exist...")
    try:
        sql_script_path = os.path.join(PROJECT_ROOT, 'sql', 'create_tables.sql')
        with open(sql_script_path, "r") as f:
            # Read the entire file content
            ddl_script = f.read()
        
        # Split the script into individual statements using the semicolon
        statements = ddl_script.split(';')
        
        with engine.connect() as connection:
            # Execute each statement one by one
            for statement in statements:
                # Ensure the statement is not just whitespace
                if statement.strip():
                    connection.exec_driver_sql(statement)
        
        print("Database and tables are ready.")
    except Exception as e:
        print(f"An error occurred during table creation: {e}")
        raise