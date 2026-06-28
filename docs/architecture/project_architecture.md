# Project Architecture

## Overview

The AI Retail Demand Forecasting Copilot follows a modular production architecture.

Each business capability is implemented as an independent package with a single responsibility.

The project follows an **experiment-first, production-second** workflow, where every completed experiment is gradually migrated into production-quality code.

---

# Planned System Architecture

```
                        +----------------------+
                        |   Raw Retail Data    |
                        +----------+-----------+
                                   |
                                   v
                  +-------------------------------+
                  | Dataset Construction          |
                  +---------------+---------------+
                                  |
                                  v
                  +-------------------------------+
                  | Processed Sales Dataset       |
                  +---------------+---------------+
                                  |
                                  v
                     +-------------------------+
                     | Demand Forecasting      |
                     |-------------------------|
                     | • Prophet              |
                     | • XGBoost              |
                     +-----------+-------------+
                                 |
                                 v
                  +-------------------------------+
                  | Inventory Analytics           |
                  +---------------+---------------+
                                  |
                                  v
                  +-------------------------------+
                  | Business Metrics              |
                  +---------------+---------------+
                                  |
                                  v
                  +-------------------------------+
                  | Knowledge Retrieval (RAG)     |
                  +---------------+---------------+
                                  |
                                  v
                  +-------------------------------+
                  | Gemini Recommendation Engine  |
                  +---------------+---------------+
                                  |
                                  v
                  +-------------------------------+
                  | Streamlit Application         |
                  +-------------------------------+
```

---

# Current Production Architecture

```
                        +----------------------+
                        |   Raw Retail Data    |
                        +----------+-----------+
                                   |
                                   v
                  +-------------------------------+
                  | Dataset Construction          |
                  +---------------+---------------+
                                  |
                                  v
                  +-------------------------------+
                  | Processed Sales Dataset       |
                  +---------------+---------------+
                                  |
                                  v
                     +-------------------------+
                     | Prophet Forecasting     |
                     +-----------+-------------+
                                 |
                     +-----------+-------------+
                     |                         |
                     v                         v
             Cross Validation          Holdout Evaluation
                     |                         |
                     +-----------+-------------+
                                 |
                                 v
                     Forecast Visualizations
                                 |
                                 v
                     Forecast Output Files
```

---

# Current Source Structure

```
src/
├── analysis/
├── data/
├── features/
├── forecasting/
│   ├── prophet/
│   │   ├── model.py
│   │   ├── pipeline.py
│   │   ├── validator.py
│   │   ├── evaluator.py
│   │   └── visualizer.py
│   │
│   └── xgboost/
│
├── inventory/
├── metrics/
├── rag/
├── recommendation/
│
├── config.py
└── main.py
```

---

# Forecasting Package Design

Each forecasting model follows the same architecture.

```
forecasting/
└── <model>/
    ├── model.py
    ├── pipeline.py
    ├── validator.py
    ├── evaluator.py
    └── visualizer.py
```

## Responsibilities

### model.py

Encapsulates the forecasting model.

---

### pipeline.py

Coordinates the complete forecasting workflow.

---

### validator.py

Performs model validation using time-series cross-validation.

---

### evaluator.py

Calculates forecasting performance metrics.

---

### visualizer.py

Creates forecast visualizations.

---

# Configuration

All project configuration is centralized in:

```
src/config.py
```

Configuration includes:

- File paths
- Forecast settings
- Input datasets
- Output locations

---

# Design Principles

The production codebase follows these principles:

- Modular architecture
- Single Responsibility Principle
- Experiment before production
- Configuration over hardcoding
- Reusable components
- Separation of concerns
- Beginner-friendly implementation
- Production-ready documentation

---

# Current Production Status

| Module | Status |
|--------|--------|
| Dataset Construction | Complete |
| Prophet Forecasting | Complete |
| XGBoost Forecasting | Next Stage |

---

# Future Architecture

The following modules will be integrated after the forecasting layer is completed:

- Inventory Analytics
- Business Metrics
- Retrieval-Augmented Generation (RAG)
- Gemini Recommendation Engine
- Streamlit Application