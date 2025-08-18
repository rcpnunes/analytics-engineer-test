import pandas as pd

def run_quality_checks(df: pd.DataFrame, table_name: str):
    """
    Orchestrates the execution of all data quality checks for a given DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to be checked.
        table_name (str): The name of the table this DataFrame represents.
    
    Raises:
        ValueError: If any of the data quality checks fail.
    """
    print(f"\n--- Running Data Quality Checks for '{table_name}' ---")
    
    # Check 1: No empty data
    if df.empty:
        raise ValueError(f"Data quality check failed: DataFrame for '{table_name}' is empty.")
    
    # Check 2: No missing values in key columns
    if table_name == 'coffee_sales':
        key_columns = ['date', 'sales_volume_bags', 'coffee_arabica_price']
    elif table_name == 'currency_rates':
        key_columns = ['date', 'currency', 'rate']
    else:
        key_columns = df.columns

    if df[key_columns].isnull().values.any():
        raise ValueError(f"Data quality check failed: Missing values found in key columns for '{table_name}'.")

    # Check 3: Data types are correct
    # (Pandas handles this well, but for more complex scenarios, this is where you'd check dtypes)

    # Check 4: Specific value checks
    if table_name == 'coffee_sales':
        if not (df['sales_volume_bags'] > 0).all() or not (df['coffee_arabica_price'] > 0).all():
            raise ValueError("Data quality check failed: Sales volume and price must be positive.")
    
    if table_name == 'currency_rates':
        expected_currencies = ['BRL', 'EUR', 'CLP']
        if not all(currency in expected_currencies for currency in df['currency'].unique()):
            raise ValueError(f"Data quality check failed: Unexpected currency found. Expected: {expected_currencies}")

    print("All data quality checks passed.")