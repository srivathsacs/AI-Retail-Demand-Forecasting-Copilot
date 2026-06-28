# Stage 3 - Prophet Forecasting

## Objective

Develop a production-ready Prophet forecasting pipeline for retail demand forecasting.

---

## Business Goal

Generate accurate demand forecasts for a selected Store–Category combination to support inventory planning and replenishment decisions.

---

## Input

- `data/processed/sales_by_category.csv`

---

## Outputs

### Forecast Files

```
data/forecasts/prophet/
├── prophet_holdout_predictions.csv
└── prophet_cv_metrics.csv
```

### Visualizations

- Prophet Trend
- Weekly Seasonality
- Yearly Seasonality
- Forecast vs Actual
- Prediction Interval

---

## Production Architecture

```
src/
└── forecasting/
    └── prophet/
        ├── model.py
        ├── pipeline.py
        ├── validator.py
        ├── evaluator.py
        └── visualizer.py
```

---

## Module Responsibilities

### model.py

Responsible for:

- Creating the Prophet model
- Configuring seasonality
- Adding external regressors
- Training
- Prediction

---

### pipeline.py

Responsible for:

- Loading processed data
- Selecting Store–Category
- Preparing Prophet dataset
- Train/Test split
- Running the forecasting workflow
- Saving holdout predictions

---

### validator.py

Responsible for:

- Time-series cross-validation
- Saving cross-validation metrics

---

### evaluator.py

Responsible for calculating:

- MAE
- RMSE
- MAPE

MAPE ignores rows where actual sales are zero.

---

### visualizer.py

Responsible for:

- Prophet component plots
- Actual vs Forecast plot
- Prediction intervals

---

## Configuration

Project configuration is centralized in:

```
src/config.py
```

Current configurable values include:

- Store ID
- Product Category
- Train/Test Split Date
- Input Paths
- Output Paths

---

## Validation

The production pipeline successfully performs:

- Dataset loading
- Prophet training
- Forecast generation
- Holdout evaluation
- Cross-validation
- Prediction visualization
- Automatic output generation

---

## Lessons Learned

The experiment consisted of one large script.

During productionization it was divided into multiple modules, each with a single responsibility.

Benefits:

- Easier maintenance
- Better readability
- Easier testing
- Cleaner architecture
- Reusable components

---

## Production Improvements

Compared to the experiment:

- Modular architecture
- Production entry point
- Centralized configuration
- Automatic output generation
- Modern scikit-learn compatibility
- Improved MAPE calculation
- Cleaner visualizations
- Type hints
- Docstrings
- Recruiter-friendly documentation

---

## Status

✅ Production Complete