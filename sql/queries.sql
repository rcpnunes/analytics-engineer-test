-- sql/queries.sql

-- Query 1: Day with the highest total sales volume and the exchange rates on that day.
-- Uses a window function (ROW_NUMBER) to rank sales for each day and select only #1.
WITH RankedSales AS (
    SELECT
        date,
        sales_volume_bags,
        -- Ranks sales within each day, from highest to lowest
        ROW_NUMBER() OVER(PARTITION BY date ORDER BY sales_volume_bags DESC) as sale_rank
    FROM
        coffee_sales
)
SELECT
    rs.date,
    rs.sales_volume_bags AS largest_sale_of_the_day,
    cr.currency,
    cr.rate
FROM
    RankedSales AS rs
JOIN
    currency_rates AS cr ON rs.date = cr.date
WHERE
    rs.sale_rank = 1 -- Filters to select only the largest sale of each day
    AND cr.currency IN ('BRL', 'EUR', 'CLP')
ORDER BY
    rs.date;

-- Query 2: Total coffee volume traded per year and the average annual exchange rate.
WITH AnnualVolume AS (
    SELECT
        STRFTIME('%Y', date) AS trade_year,
        SUM(sales_volume_bags) AS total_annual_volume
    FROM
        coffee_sales
    GROUP BY
        trade_year
),
AnnualRates AS (
    SELECT
        STRFTIME('%Y', date) AS trade_year,
        AVG(CASE WHEN currency = 'BRL' THEN rate END) AS avg_rate_brl,
        AVG(CASE WHEN currency = 'EUR' THEN rate END) AS avg_rate_eur,
        AVG(CASE WHEN currency = 'CLP' THEN rate END) AS avg_rate_clp
    FROM
        currency_rates
    GROUP BY
        trade_year
)
SELECT
    av.trade_year,
    av.total_annual_volume,
    ar.avg_rate_brl,
    ar.avg_rate_eur,
    ar.avg_rate_clp
FROM
    AnnualVolume AS av
JOIN
    AnnualRates AS ar ON av.trade_year = ar.trade_year
ORDER BY
    av.trade_year;


-- Query 3: Average total traded volume per day (grouped by month and year).
-- Logic: First, we create a view of the total daily volume.
-- Then, we calculate the average of these daily totals for each month and each year.
WITH DailyVolume AS (
    SELECT
        date,
        SUM(sales_volume_bags) AS total_daily_volume
    FROM
        coffee_sales
    GROUP BY
        date
)
-- Monthly Average of Daily Volume
SELECT
    'Monthly' AS period_type,
    STRFTIME('%Y-%m', date) AS period,
    AVG(total_daily_volume) AS avg_daily_volume
FROM
    DailyVolume
GROUP BY
    period

UNION ALL

-- Annual Average of Daily Volume
SELECT
    'Annual' AS period_type,
    STRFTIME('%Y', date) AS period,
    AVG(total_daily_volume) AS avg_daily_volume
FROM
    DailyVolume
GROUP BY
    period
ORDER BY
    period_type, period;