from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.append(
    str(PROJECT_ROOT)
)


from src.forecasting.xgboost_model import (
    XGBoostForecaster
)

print("SUCCESS")