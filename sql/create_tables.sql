-- Coffee sales table
CREATE TABLE IF NOT EXISTS coffee_sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    sales_volume_bags REAL,
    coffee_arabica_price REAL
);

-- Exchange rates table
CREATE TABLE IF NOT EXISTS currency_rates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    currency TEXT,
    rate REAL,
    UNIQUE(date, currency)
);

-- Newer table to store the latest currency rates
CREATE TABLE IF NOT EXISTS latest_currency_rates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    currency TEXT,
    rate REAL,
    UNIQUE(date, currency)
);