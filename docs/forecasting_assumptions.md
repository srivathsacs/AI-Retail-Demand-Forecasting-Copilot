# Forecasting Assumptions

This document records the assumptions used during development of the demand forecasting system.

The purpose is to ensure forecasting logic remains understandable, reproducible, and free from data leakage.

---

# Assumption 1: Future Promotion Information Is Available

## Description

The XGBoost model uses `promotion_count` as an input feature.

This assumes future promotion plans are known before forecasts are generated.

Example:

* Marketing schedules promotions for next week.
* Promotion plans are available to the forecasting system.
* The model uses planned promotion activity when generating forecasts.

## Why This Matters

If future promotions are unknown at forecast time, then `promotion_count` cannot be used directly.

In that case:

* promotion activity must be forecast separately, or
* the feature must be removed from the forecasting model.

## Current Project Status

Future promotion information is assumed to be available.

Therefore `promotion_count` is treated as a valid forecasting feature.

---

# Assumption 1A: Future Promotion Schedules Are Supplied Through Business Inputs

## Description

Stage 4.5 introduced a production forecasting layer capable of generating future demand forecasts.

The forecasting engine requires future promotion activity because `promotion_count` is part of the final production feature set.

Future promotion schedules are supplied through:

```text
data/future_promotions.csv
```

## Portfolio Implementation

Because actual future promotion plans are unavailable in the Kaggle dataset, a demonstration promotion schedule is used.

Rules:

* Weekdays = 25 promotions
* Weekends = 50 promotions

These values were selected using historical promotion behavior observed in the Store 44 + GROCERY I series.

Historical Statistics:

* Mean promotion_count ≈ 28
* Median promotion_count = 10
* 75th percentile = 50

## Why This Matters

This approach keeps production forecasting consistent with model training.

The model was trained using:

* promotion_count
* calendar features
* lag features
* rolling features

Removing promotion_count during forecasting would create a train-serve mismatch.

## Future Production State

Future promotion schedules should originate from retail planning systems, marketing calendars, or promotion management platforms rather than static files.

## Current Project Status

Future promotion schedules are supplied through:

```text
data/future_promotions.csv
```

and consumed by the recursive forecasting engine.

---

# Assumption 2: Lag Features Use Only Historical Information

## Description

The forecasting model may use lag features such as:

* lag_1
* lag_7
* lag_14
* lag_28

These features represent sales observed in the past.

Examples:

* lag_1 = sales from 1 day ago
* lag_7 = sales from 7 days ago
* lag_28 = sales from 28 days ago

## Leakage Prevention

Lag features are generated using Pandas `shift()` operations.

Example:

```python
df["lag_7"] = df["sales"].shift(7)
```

This ensures each observation only uses information that would have been available at the prediction timestamp.

Example:

For 2017-07-15:

* lag_7 uses sales from 2017-07-08

No future sales values are used.

## Current Project Status

Lag features are considered leakage-safe.

---

# Assumption 3: Feature Generation Strategy

## Description

Lag features are generated on the full chronologically sorted series before train/test splitting.

Workflow:

Sort Series
→ Create Lag Features
→ Train/Test Split
→ Model Training

## Why This Is Safe

Lag features are based entirely on historical observations through the use of `shift()`.

No future observations are used when constructing lag values.

## Industry Practice

This approach is commonly used in forecasting pipelines and is considered safe when all lag and rolling features rely exclusively on past observations.

---

# Assumption 4: Single-Series Development

## Description

Model development currently focuses on a single forecasting series:

Store 44 + GROCERY I

## Reason

Using one series simplifies:

* demand analysis
* feature engineering
* debugging
* model comparison

## Future State

The final system should scale to all store-category combinations.

---

# Assumption 5: Holdout Evaluation Represents Future Performance

## Description

Models are evaluated using a time-based split.

Train Period:

Before 2017-07-01

Test Period:

On or After 2017-07-01

## Purpose

This simulates real forecasting where future observations are unavailable during model training.

## Current Project Status

All forecasting decisions are based on:

* Rolling Time-Series Cross Validation
* Holdout Evaluation
* MAE
* RMSE
* MAPE

rather than training performance alone.

---

# Assumption 6: Recursive Forecasting Uses Predicted Demand

## Description

The production forecasting engine generates multi-step forecasts using recursive forecasting.

For future dates, lag and rolling features cannot rely on unknown future sales.

Instead:

1. Predict Day 1 demand
2. Append prediction to forecasting history
3. Recalculate lag and rolling features
4. Predict Day 2 demand
5. Repeat until the forecast horizon is complete

## Why This Matters

The final XGBoost model relies on:

* lag_1
* lag_7
* lag_14
* lag_28
* rolling_mean_7
* rolling_mean_28

Recursive forecasting allows these features to remain available beyond the last observed date.

## Current Project Status

Recursive forecasting is implemented within:

```text
src/forecasting/xgboost_model.py
```

and is used to generate future demand forecasts.

---

# Future Production Improvements

The current project uses:

* Single-series forecasting
* Static future promotion schedules
* Point forecasts

Future production versions should consider:

* multi-series forecasting
* automated retraining pipelines
* promotion forecasting
* probabilistic forecasting
* hierarchical forecasting

to better simulate real-world forecasting operations.

---

# Core Forecasting Principle

A forecasting feature is valid only if the same information would be available when generating future forecasts in production.


# Assumption 7: Current Inventory Information Is Available

## Description

The Inventory Position Engine introduced in Stage 5 requires current inventory levels when evaluating future inventory conditions.

Example:

```text
Current Inventory = 500,000 units
```

This value represents inventory available at the time the forecast is generated.

## Why This Matters

Forecast demand alone cannot determine inventory risk.

The system must compare:

```text
Current Inventory
-
Forecast Demand
```

to estimate future inventory levels.

Without current inventory information:

* projected inventory cannot be calculated
* inventory gap cannot be calculated
* stockout risk cannot be evaluated

## Current Project Status

Current inventory is supplied manually during Stage 5 testing.

Example:

```text
Current Inventory = 500,000
```

## Future Production State

Current inventory should originate from:

* ERP systems
* Inventory Management Systems
* Warehouse Management Systems

rather than manual inputs.

---

# Assumption 8: Safety Stock Values Are Available

## Description

The Risk Engine relies on safety stock to determine inventory risk levels.

Example:

```text
Safety Stock = 50,000 units
```

Safety stock represents inventory reserved to protect against uncertainty.

Examples:

* demand spikes
* forecast error
* supplier delays
* replenishment disruptions

## Why This Matters

Inventory risk is evaluated relative to safety stock rather than inventory alone.

Example:

Inventory Remaining:

```text
56,152 units
```

may appear safe.

However:

```text
Safety Stock = 50,000
```

means only:

```text
6,152 units
```

remain above the protection threshold.

This produces a different business interpretation.

## Current Project Status

Safety stock is supplied manually during Stage 5 testing.

## Future Production State

Safety stock should be generated through:

* service-level targets
* lead-time variability
* demand variability models

---

# Assumption 9: Lead Time Is Known

## Description

Inventory planning metrics rely on replenishment lead time.

Example:

```text
Lead Time = 30 Days
```

Lead time represents the period between placing an order and receiving inventory.

## Why This Matters

Lead time is required for:

* Lead Time Demand
* Reorder Point
* Recommended Order Quantity

calculations.

## Current Project Status

Lead time is provided manually during Stage 6 testing.

## Future Production State

Lead time should originate from supplier and procurement systems.

---

# Assumption 10: Business Metrics Are Decision-Support Metrics

## Description

Stage 6 introduces business-facing metrics including:

* Potential Lost Sales
* Revenue Risk
* Inventory At Risk
* Recommended Order Quantity
* Inventory Health Score

These metrics are designed to support planning decisions.

## Why This Matters

The metrics are intended for:

* inventory planning
* replenishment decisions
* risk communication

They are not intended to replace:

* audited financial reports
* accounting systems
* ERP financial calculations

## Current Project Status

Business metrics are treated as planning metrics rather than official financial measures.

---

# Assumption 11: Inventory Health Score Is A Heuristic Metric

## Description

Inventory Health Score is designed as a business-friendly summary indicator.

The score combines:

* Stockout Risk
* Overstock Risk
* Safety Stock Breach Status

into a single value.

## Why This Matters

The score simplifies interpretation of multiple inventory signals.

Example:

```text
Inventory Health Score = 80
```

is easier for managers to interpret than multiple risk variables.

## Current Project Status

The score is generated using a rule-based penalty framework.

Example:

```text
Start at 100

MEDIUM Stockout Risk
=
-20

Final Score
=
80
```

## Future Production State

Future versions may replace the rule-based approach with:

* service-level models
* simulation-based scoring
* probabilistic inventory risk measures
