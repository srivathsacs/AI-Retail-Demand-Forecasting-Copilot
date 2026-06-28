"""
Create category-level daily sales dataset from raw transaction data.

Input:
    train.csv
    items.csv

Output:
    sales_by_category.csv

Grain:
    One row per day, store, and category.
"""

import duckdb

# Aggregate SKU-level transactions to category level
# Count promoted items per day/store/category
# Export curated forecasting dataset

duckdb.sql("""
COPY (
    SELECT
        t.date,
        t.store_nbr AS store_id,
        i.family AS category,
        SUM(t.unit_sales) AS sales,
        SUM(
            CASE
                WHEN t.onpromotion = TRUE THEN 1
                ELSE 0
            END
        ) AS promotion_count
    FROM 'data/raw/train.csv' t
    JOIN 'data/raw/items.csv' i
        ON t.item_nbr = i.item_nbr
    GROUP BY
        t.date,
        t.store_nbr,
        i.family
)
TO 'data/processed/sales_by_category.csv'
WITH (HEADER, DELIMITER ',');
""")

print("sales_by_category.csv created successfully")