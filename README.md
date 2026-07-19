````markdown
# AI Retail Demand Forecasting Copilot

## Overview

AI Retail Demand Forecasting Copilot is an end-to-end AI decision support system for retail inventory planning.

The project combines demand forecasting, inventory analytics, Retrieval-Augmented Generation (RAG), and Generative AI to help retailers make better inventory decisions.

The project follows an **experiment-first, production-second** workflow, where every feature is:

1. Developed and validated in the `experiments/` folder.
2. Migrated into modular production code under `src/`.
3. Documented before moving to the next development stage.

---

# Planned System Architecture

```
Raw Retail Data
        │
        ▼
Dataset Construction
        │
        ▼
Demand Forecasting
   ├── Prophet
   └── XGBoost
        │
        ▼
Inventory Analytics
        │
        ▼
Business Metrics
        │
        ▼
Knowledge Retrieval (RAG)
        │
        ▼
AI Recommendation Engine
        │
        ▼
Streamlit Application
```

---

# Current Project Status

| Stage | Status |
|--------|--------|
| Dataset Construction | Complete |
| Exploratory Data Analysis | Complete |
| Prophet Forecasting | Complete |
| XGBoost Forecasting | Complete |
| Inventory Analytics | Complete |

---

# Current Production Structure

```
src/
├── analysis/
├── data/
├── features/
├── forecasting/
│   ├── prophet/
│   └── xgboost/
├── inventory/
├── metrics/
├── rag/
├── recommendation/
├── config.py
└── main.py
```

---

# Current Features

- Production dataset construction pipeline
- Centralized project configuration
- Modular Prophet forecasting package
- Modular XGBoost forecasting package
- Production Inventory Analytics package
- Inventory position calculation
- Inventory risk assessment
- Structured inventory analysis output
- Rolling time-series cross-validation
- Holdout forecasting evaluation
- Forecast performance metrics
- Forecast visualization
- Automatic forecast export
- Production-ready documentation

---

# Technology Stack

## Programming

- Python

## Data Engineering

- Pandas
- DuckDB

## Forecasting

- Prophet
- XGBoost

## Artificial Intelligence

- Google Gemini
- LangChain

## Vector Database

- ChromaDB

## Embeddings

- Sentence Transformers
- all-MiniLM-L6-v2

## Frontend

- Streamlit

---

# Repository Structure

```
data/
docs/
experiments/
src/
README.md
requirements.txt
```

---

# Dataset

This project uses the **Corporación Favorita Grocery Sales Forecasting** dataset from Kaggle.

The dataset is not included in this repository.

Download the required dataset from Kaggle and place the CSV files in:

```text
data/raw/
```

Required files:

- `train.csv`
- `items.csv`

All processed datasets, forecasts, and other generated outputs are created locally during project execution.

---

# Prerequisites

Before running the project, ensure the following are installed:

- Python 3.11 or later
- Git

A virtual environment is recommended for dependency isolation.

---

# Installation

Clone the repository:

```bash
git clone <repository-url>
cd AI-Retail-Demand-Forecasting-Copilot
```

Create and activate a virtual environment.

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

# Dataset Setup

Download the **Corporación Favorita Grocery Sales Forecasting** dataset from Kaggle.

Place the required files inside:

```text
data/raw/
```

Required files:

- `train.csv`
- `items.csv`

---

# Documentation

Project documentation is available under:

```text
docs/
```

Current documentation includes:

- Production stage documentation
- Project architecture

---

# Running the Project

From the project root, run:

```bash
python src/main.py
```

The production pipeline automatically executes:

1. Dataset Construction
2. Prophet Forecasting
3. XGBoost Forecasting
4. Inventory Analytics

The console displays:

- Cross-validation metrics
- Holdout evaluation metrics
- Inventory position
- Inventory gap
- Stockout risk
- Overstock risk
- Risk severity

Forecast visualizations are generated automatically during execution.

---

# Generated Outputs

Running the project automatically creates:

- Processed category sales dataset
- Prophet holdout predictions
- Prophet cross-validation metrics
- XGBoost holdout predictions
- XGBoost cross-validation metrics
- Inventory analytics results

Generated files are stored locally under the project's `data/` directory.

---

# Development Workflow

Every feature follows the same development lifecycle.

```
Experiment
      │
      ▼
Validation
      │
      ▼
Production Implementation
      │
      ▼
Documentation
```

---

# Roadmap

## Next Development Stages

- Business Metrics
- Retrieval-Augmented Generation (RAG)
- AI Recommendation Engine
- Streamlit Application

## Future Enhancements

- Logging framework
- Unit testing
- Integration testing
- Continuous Integration (CI)
- Docker support
- Cloud deployment

---

# License

This project is intended for educational and portfolio purposes.
````
