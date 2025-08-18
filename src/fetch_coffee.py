import os
import pandas as pd
from dotenv import load_dotenv
import kagglehub

# Load environment variables
load_dotenv()

# --- Constants ---
DATASET_HANDLE = "utkarshx27/select-world-bank-commodity-price-data"
# Corrected the filename as you pointed out
FILE_NAME_IN_DATASET = "commodity_prices.csv"
# The final, correct destination for our single file
LOCAL_FILE_PATH = "data/coffee.csv"


def fetch_and_load_coffee_data(handle: str, file_name: str) -> pd.DataFrame:
    """
    Downloads a dataset from Kaggle, finds a specific CSV file within it,
    and loads it into a pandas DataFrame.
    """
    print(f"Attempting to download dataset '{handle}' from Kaggle Hub...")
    try:
        download_path = kagglehub.dataset_download(handle)
        csv_file_path = os.path.join(download_path, file_name)
        
        print(f"Dataset downloaded to temporary cache: {download_path}")
        print(f"Loading ONLY the file: {csv_file_path}")

        if os.path.exists(csv_file_path):
            df = pd.read_csv(csv_file_path)
            print("Data loaded successfully into a DataFrame.")
            return df
        else:
            print(f"Error: The file '{file_name}' was not found.")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    df_raw = fetch_and_load_coffee_data(
        handle=DATASET_HANDLE,
        file_name=FILE_NAME_IN_DATASET
    )

    if df_raw is not None:
        # 1. Select only the required columns. Note the original names from the CSV.
        print("\nFiltering for 'Date' and 'Coffee Arabica' columns...")
        df_filtered = df_raw[['date', 'coffee_arabica']].copy()
        
        # 3. Save the final, transformed DataFrame.
        os.makedirs("data", exist_ok=True)
        df_filtered.to_csv(LOCAL_FILE_PATH, index=False)
        print(f"\nSUCCESS! Final file with selected columns saved to: '{LOCAL_FILE_PATH}'")

        print("\n--- Final Coffee Data Head ---")
        print(df_filtered.head())
        print("\n--- Final Coffee Data Info ---")
        df_filtered.info()

# Run python src/fetch_coffee.py in terminal to execute this script.
# Ensure you have the Kaggle Keys are set in the .env file.