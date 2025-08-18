import pandas as pd
from db import get_engine, create_database_and_tables
from quality import run_quality_checks

# --- Added constant for the new file ---
LATEST_CURRENCY_PATH = "data/currency_rates.csv"
HISTORICAL_COFFEE_PATH = "data/coffee_sales_historical.csv"
HISTORICAL_CURRENCY_PATH = "data/currency_rates_historical.csv"

def load_data_to_db():
    print("Starting data loading process...")
    engine = get_engine()
    create_database_and_tables(engine)
    
    # Read all 3 data files
    df_latest_currency = pd.read_csv(LATEST_CURRENCY_PATH)
    df_historical_coffee = pd.read_csv(HISTORICAL_COFFEE_PATH)
    df_historical_currency = pd.read_csv(HISTORICAL_CURRENCY_PATH)
    
    # --- Run Quality Checks on all DataFrames ---
    try:
        run_quality_checks(df_latest_currency, 'currency_rates') # Reuse the same rules
        run_quality_checks(df_historical_coffee, 'coffee_sales')
        run_quality_checks(df_historical_currency, 'currency_rates')
    except ValueError as e:
        print(f"Data quality check failed: {e}")
        return # Stop the process if data quality is not met
    
    # --- Load data into SQLite tables ---
    try:
        # Load recent data into the new table
        print(f"\nLoading latest currency data into 'latest_currency_rates' table...")
        df_latest_currency.to_sql('latest_currency_rates', con=engine, if_exists='replace', index=False)
        print("Latest currency data loaded successfully.")
        
        # Load historical data (no change)
        print(f"Loading coffee sales data into 'coffee_sales' table...")
        df_historical_coffee.to_sql('coffee_sales', con=engine, if_exists='replace', index=False)
        print("Coffee sales data loaded successfully.")
        
        print(f"Loading historical currency data into 'currency_rates' table...")
        df_historical_currency.to_sql('currency_rates', con=engine, if_exists='replace', index=False)
        print("Historical currency data loaded successfully.")
        
    except Exception as e:
        print(f"An error occurred while loading data: {e}")
        raise

    print("\nData loading process finished successfully!")

if __name__ == "__main__":
    load_data_to_db()