# Stage 1 - Dataset Construction

## Objective

Build a clean, category-level sales dataset from the raw retail data.

---

## Input

- `data/raw/train.csv`
- `data/raw/items.csv`

---

## Output

- `data/processed/sales_by_category.csv`

---

## Production Files

- `src/config.py`
- `src/main.py`
- `src/data/dataset_builder.py`

---

## Processing Steps

1. Load transaction data.
2. Load item metadata.
3. Join both datasets using `item_nbr`.
4. Aggregate sales by:
   - Date
   - Store
   - Product Category
5. Count promoted items.
6. Save the processed dataset.

---

## Output Columns

| Column | Description |
|---------|-------------|
| date | Sales date |
| store_id | Store number |
| category | Product category |
| sales | Total daily sales |
| promotion_count | Number of promoted items |

---

## Validation

- Production pipeline executed successfully.
- Dataset generated successfully.
- Output file overwritten as expected.
- No business logic changes from the experiment.

---

## Status

✅ Complete