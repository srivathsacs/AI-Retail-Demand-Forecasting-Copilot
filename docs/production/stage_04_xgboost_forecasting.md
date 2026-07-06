# Stage 4 — XGBoost Forecasting

## Overview

This stage migrates the experimental XGBoost forecasting workflow into the production codebase.

The implementation follows the same modular architecture established during the Prophet production migration, making both forecasting approaches consistent and interchangeable.

---

## Objectives

- Build a production-ready XGBoost forecasting package.
- Separate responsibilities into modular components.
- Evaluate forecasting performance using rolling time-series cross-validation.
- Evaluate final performance on an unseen holdout dataset.
- Save forecasting outputs for downstream analysis.

---

## Production Package

```
src/
└── forecasting/
    └── xgboost/
        ├── __init__.py
        ├── model.py
        ├── pipeline.py
        ├── validator.py
        ├── evaluator.py
        └── visualizer.py
```

---

## Module Responsibilities

### model.py

Encapsulates the XGBoost model.

Responsibilities:

- Initialize the XGBoost regressor.
- Train the model.
- Generate predictions.

---

### pipeline.py

Executes the end-to-end forecasting workflow.

Responsibilities:

- Load processed data.
- Filter a store/category.
- Create calendar features.
- Create lag features.
- Create rolling mean features.
- Split train and holdout datasets.
- Train the model.
- Generate holdout predictions.
- Save prediction outputs.

---

### validator.py

Performs rolling time-series cross-validation.

Responsibilities:

- Generate rolling cutoff dates.
- Train multiple forecasting models.
- Evaluate each forecasting window.
- Save cross-validation metrics.

---

### evaluator.py

Calculates forecasting accuracy metrics.

Metrics:

- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- Mean Absolute Percentage Error (MAPE)

---

### visualizer.py

Visualizes forecasting results.

Displays:

- Actual sales
- Predicted sales

---

## Validation Strategy

Two evaluation approaches are used.

### Rolling Cross-Validation

Evaluates forecasting performance across multiple historical forecasting windows.

Reported metrics:

- MAE
- RMSE
- MAPE

---

### Holdout Evaluation

Evaluates the final production model using unseen data after the train/test split.

Reported metrics:

- MAE
- RMSE
- MAPE

---

## Hyperparameter Optimization

The production XGBoost model uses the best-performing hyperparameters identified during the experimental Optuna-based hyperparameter optimization stage.

The optimization objective minimized the average Mean Absolute Percentage Error (MAPE) obtained from rolling time-series cross-validation.

Only the final optimized hyperparameters were migrated into the production code. The optimization workflow remains part of the experimental codebase.

## Outputs

Generated files:

```
data/forecasts/

├── xgboost_holdout_predictions.csv
└── xgboost_cv_metrics.csv
```

---

## Stage Summary

Stage 4 introduces a production-ready XGBoost forecasting pipeline that follows the same modular architecture as the Prophet implementation while providing an additional machine learning forecasting approach for retail demand prediction.