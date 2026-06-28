"""
Explore a single forecasting series.

Goals:
- Visualize sales history
- Identify trend
- Identify seasonality
- Understand demand behavior before modeling
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/processed/sales_by_category.csv")

series = df[
    (df["store_id"] == 44) &
    (df["category"] == "GROCERY I")
].copy()

series["date"] = pd.to_datetime(series["date"])
series = series.sort_values("date")

plt.figure(figsize=(12, 5))
plt.plot(series["date"], series["sales"])

plt.title("Store 44 - GROCERY I")
plt.xlabel("Date")
plt.ylabel("Sales")

plt.show()