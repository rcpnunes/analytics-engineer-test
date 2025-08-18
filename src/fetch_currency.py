import os
import time
import requests
import pandas as pd
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CURRENCYLAYER_API_KEY")
BASE_URL = "http://api.currencylayer.com"
CURRENCIES = ["BRL", "EUR", "CLP", "USD"]

if not API_KEY:
    raise EnvironmentError(
        "Missing CURRENCYLAYER_API_KEY in environment variables. "
        "Please set it in the .env file."
    )

def fetch_exchange_rate(date: str) -> dict:
    """
    Fetch exchange rates for a specific date from CurrencyLayer API.
    """
    endpoint = f"{BASE_URL}/historical"
    params = {
        "access_key": API_KEY,
        "date": date,
        "currencies": ",".join(CURRENCIES),
        "format": 1
    }

    response = requests.get(endpoint, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    if not data.get("success", False):
        raise ValueError(f"API Error: {data.get('error', {}).get('info', 'Unknown error')}")

    return data["quotes"]

def fetch_last_30_days() -> pd.DataFrame:
    """
    Fetch exchange rates for the last 30 days and return as DataFrame.
    Includes a 2    to avoid hitting rate limits. Got several errors when not respecting this delay.
    Important: The free API only supports 100 requests per month. 
    The final test requires 3 years of data into a dashboard, so to bring this information it's needed to adapt the variable 'dates' below with a premium subscription.
    """
    today = datetime.now(timezone.utc).date()
    dates = [today - timedelta(days=i) for i in range(30)]
    all_data = []
    for d in dates:

        try:
            quotes = fetch_exchange_rate(d.strftime("%Y-%m-%d"))
            for k, v in quotes.items():
                all_data.append({
                    "date": d.strftime("%Y-%m-%d"),
                    "currency": k.replace("USD", ""),
                    "rate": v
                })
        except Exception as e:
            print(f"Failed to fetch {d}: {e}")

        # Delay to prevent hitting API rate limits
        time.sleep(2)

    return pd.DataFrame(all_data)

def main():
    """Main function to fetch and save currency rates."""
    print("--- Fetching Currency Data ---")
    df_rates = fetch_last_30_days()
    output_path = "data/currency_rates.csv"
    os.makedirs("data", exist_ok=True)
    df_rates.to_csv(output_path, index=False)
    print(f"Currency rates saved to {output_path}\n")

if __name__ == "__main__":
    main()

# Run python src/fetch_currency.py in terminal to execute this script.
# Ensure you have the CURRENCYLAYER_API_KEY set in the .env file.