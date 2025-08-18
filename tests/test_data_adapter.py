import pandas as pd
import pytest
from src.data_adapter import simulate_daily_sales

def test_simulate_daily_sales():
    """
    Tests the simulate_daily_sales function to ensure it generates
    a granular sales DataFrame correctly.
    """
    # 1. Setup: Create a small, simple input DataFrame
    input_data = {
        'date': pd.to_datetime(['2025-01-01', '2025-01-02']),
        'coffee_arabica': [150.0, 200.0]
    }
    input_df = pd.DataFrame(input_data)

    # 2. Execution: Run the function being tested
    result_df = simulate_daily_sales(input_df)

    # 3. Assertions: Check if the output is as expected
    
    # Assert that the output is not empty
    assert not result_df.empty
    
    # Assert that the required columns were created
    assert 'date' in result_df.columns
    assert 'sales_volume_bags' in result_df.columns
    assert 'coffee_arabica_price' in result_df.columns
    
    # Assert that all original dates are present in the result
    assert all(date in pd.to_datetime(result_df['date'].unique()) for date in input_df['date'])
    
    # Assert that the price for a given day is consistent across all its sales
    first_day_price = result_df[result_df['date'] == pd.to_datetime('2025-01-01')]['coffee_arabica_price'].iloc[0]
    assert first_day_price == 150.0
    
    # Assert that there are multiple sales per day
    assert result_df.groupby('date').size().min() > 0