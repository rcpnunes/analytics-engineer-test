"""
PIPELINE ORCHESTRATOR

This is the main entry point for running the entire ETL and upload pipeline.
It executes the necessary scripts in the correct sequence.
"""

import sys
import os

# This line allows the script to find and import modules from the 'src' directory
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Now we can import the main functions from our scripts
from fetch_currency import main as run_currency_fetch
from data_adapter import main as run_data_adapter
from load import load_data_to_db
from transform import execute_transformations
from upload_to_drive import upload_files_to_drive


def run_pipeline():
    """
    Executes the full data pipeline in the correct order.
    """
    print(" --- STARTING FULL DATA PIPELINE --- ")
    
    try:
        # Step 1: Fetch the latest currency data from the API
        print("\n[STEP 1/5] Fetching latest currency rates...")
        run_currency_fetch()
        
        # Step 2: Generate historical data using the data adapter
        print("\n[STEP 2/5] Generating historical data...")
        run_data_adapter()

        # Step 3: Load the historical data into the SQLite database
        print("\n[STEP 3/5] Loading data into database...")
        load_data_to_db()

        # Step 4: Run SQL transformations to get final analytical results
        print("\n[STEP 4/5] Executing SQL transformations...")
        execute_transformations()

        # Step 5: Upload the final CSVs to Google Drive
        print("\n[STEP 5/5] Uploading results to Google Drive...")
        upload_files_to_drive()

        print("\n --- PIPELINE COMPLETED SUCCESSFULLY --- ")

    except Exception as e: # Errors during any step will be caught here
        # If any step fails, we print the error and stop the pipeline
        print(f"\n --- PIPELINE FAILED --- ")
        print(f"An error occurred: {e}")
        
        
if __name__ == "__main__":
    run_pipeline()