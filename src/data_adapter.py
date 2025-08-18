# -*- coding: utf-8 -*-
"""
DATA ADAPTER & SYNTHESIZER

This script is responsible for generating random & historical datasets for analysis.
It performs the following steps:
1.  Reads historical coffee price and currency exchange rate data from CSV files.
2.  Establishes a dynamic date range (from the last 2 full years up to today).
3.  Fills any data gaps within this range by generating realistic synthetic values
    based on the statistical distribution (quartiles) of the original data.
4.  Transforms the daily coffee price data into a granular table of
    sales transactions by simulating multiple sales per day with varied volumes.
5.  Saves the two generated historical datasets ('coffee_sales' and 'currency_rates')
    to new CSV files in the /data folder.
"""

import pandas as pd
import numpy as np
from datetime import datetime

# --- Constants ---
COFFEE_INPUT_PATH = "data/coffee.csv"
CURRENCY_INPUT_PATH = "data/currency_rates.csv"
COFFEE_OUTPUT_PATH = "data/coffee_sales_historical.csv"
CURRENCY_OUTPUT_PATH = "data/currency_rates_historical.csv"

# --- Dynamic Date Range ---
today = datetime.now()
START_DATE = f"{today.year - 2}-01-01"
END_DATE = today.strftime('%Y-%m-%d')


def process_coffee_data(df_orig: pd.DataFrame, date_range_df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepares the historical coffee price data for the specified date range.
    It fills any missing daily values with realistic synthetic data.

    Args:
        df_orig (pd.DataFrame): The original coffee price DataFrame from Kaggle.
        date_range_df (pd.DataFrame): A DataFrame with a single 'date' column for the full range.

    Returns:
        pd.DataFrame: A complete daily coffee price DataFrame for the specified range.
    """
    # Use the original data's statistics to create a realistic range for new data
    q1 = df_orig['coffee_arabica'].quantile(0.25)
    q3 = df_orig['coffee_arabica'].quantile(0.75)

    # Merge to align original data with the full date range, creating NaN for gaps
    df_merged = pd.merge(date_range_df, df_orig, on='date', how='left')
    
    missing_data_mask = df_merged['coffee_arabica'].isna()
    num_missing = missing_data_mask.sum()

    if num_missing > 0:
        # Generate synthetic values only for the missing dates
        random_values = np.random.uniform(low=q1, high=q3, size=num_missing)
        df_merged.loc[missing_data_mask, 'coffee_arabica'] = random_values
    
    return df_merged


def simulate_daily_sales(df_daily_prices: pd.DataFrame) -> pd.DataFrame:
    """
    Simulates granular sales transactions from aggregated daily price data.
    For each day, it creates multiple sales records with random volumes,
    using the daily price as a reference.

    Args:
        df_daily_prices (pd.DataFrame): DataFrame with one price per day.

    Returns:
        pd.DataFrame: A DataFrame with multiple sales rows per day.
    """
    print("\nSimulating granular daily sales from aggregated data...")
    new_sales_records = []

    for _, row in df_daily_prices.iterrows():
        date = row['date']
        daily_price = row['coffee_arabica']

        # Create a random number of sales transactions for the day
        num_sales = np.random.randint(1, 5)

        for _ in range(num_sales):
            # Simulate a random sales volume for this specific transaction
            sale_volume = np.random.uniform(1, 100)
            
            new_sales_records.append({
                "date": date,
                "sales_volume_bags": sale_volume,
                "coffee_arabica_price": daily_price
            })
            
    print("Simulation complete.")
    return pd.DataFrame(new_sales_records)


def process_currency_data(df_orig: pd.DataFrame, date_range_df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepares historical currency rate data for the specified date range.
    It fills any missing daily values for each currency with realistic synthetic data.

    Args:
        df_orig (pd.DataFrame): The original currency rates DataFrame.
        date_range_df (pd.DataFrame): A DataFrame with a single 'date' column for the full range.

    Returns:
        pd.DataFrame: A complete daily currency rate DataFrame for the specified range.
    """
    print("\nProcessing currency data...")
    processed_currencies = []
    
    for currency_code in df_orig['currency'].unique():
        df_single_currency = df_orig[df_orig['currency'] == currency_code]
        
        # Merge to create gaps for this specific currency
        df_merged = pd.merge(date_range_df, df_single_currency, on='date', how='left')
        
        missing_data_mask = df_merged['rate'].isna()
        num_missing = missing_data_mask.sum()

        if num_missing > 0:
            # Calculate statistics and fill gaps for this currency
            q1 = df_merged['rate'].quantile(0.25)
            q3 = df_merged['rate'].quantile(0.75)
            random_values = np.random.uniform(low=q1, high=q3, size=num_missing)
            df_merged.loc[missing_data_mask, 'rate'] = random_values
        
        # Ensure the currency code is present in all rows
        df_merged['currency'] = currency_code
        processed_currencies.append(df_merged)

    return pd.concat(processed_currencies, ignore_index=True)


def main():
    """
    Main function to orchestrate the data adaptation and synthesis process.
    """
    print(f"Starting data adaptation for date range: {START_DATE} to {END_DATE}")

    # Load original datasets
    df_coffee_orig = pd.read_csv(COFFEE_INPUT_PATH, parse_dates=['date'])
    df_currency_orig = pd.read_csv(CURRENCY_INPUT_PATH, parse_dates=['date'])
    
    # Create the base date range for the historical data
    full_date_range = pd.date_range(start=START_DATE, end=END_DATE, freq='D')
    df_full_dates = pd.DataFrame(full_date_range, columns=['date'])

    # --- Process and Simulate Coffee Data ---
    df_daily_coffee_prices = process_coffee_data(df_coffee_orig, df_full_dates)
    df_coffee_sales = simulate_daily_sales(df_daily_coffee_prices)
    df_coffee_sales.to_csv(COFFEE_OUTPUT_PATH, index=False)
    print(f"Adapted coffee sales data saved to '{COFFEE_OUTPUT_PATH}'")

    # --- Process Currency Data ---
    df_currency_final = process_currency_data(df_currency_orig, df_full_dates)
    df_currency_final.to_csv(CURRENCY_OUTPUT_PATH, index=False)
    print(f"Adapted currency data saved to '{CURRENCY_OUTPUT_PATH}'")

    # --- Final Preview ---
    print("\n--- Simulated Coffee Sales Data Head (New Format) ---")
    print(df_coffee_sales.head())
    print("\nData adaptation complete.")


if __name__ == "__main__":
    main()