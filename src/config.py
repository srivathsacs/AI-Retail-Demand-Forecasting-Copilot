"""
Module: config.py

Purpose:
    Central location for all project configuration.
"""

from pathlib import Path

# =============================================================================
# Project Paths
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
FORECAST_DIR = DATA_DIR / "forecasts"

# =============================================================================
# Input Files
# =============================================================================

TRAIN_DATA = RAW_DATA_DIR / "train.csv"
ITEMS_DATA = RAW_DATA_DIR / "items.csv"

# =============================================================================
# Processed Data
# =============================================================================

CATEGORY_SALES_DATA = PROCESSED_DATA_DIR / "sales_by_category.csv"

# =============================================================================
# Prophet Configuration
# =============================================================================

PROPHET_STORE_ID = 44

PROPHET_CATEGORY = "GROCERY I"

TRAIN_TEST_SPLIT_DATE = "2017-07-01"

# =============================================================================
# Prophet Outputs
# =============================================================================

PROPHET_HOLDOUT_PREDICTIONS = (
    FORECAST_DIR / "prophet_holdout_predictions.csv"
)

PROPHET_CV_METRICS = (
    FORECAST_DIR / "prophet_cv_metrics.csv"
)