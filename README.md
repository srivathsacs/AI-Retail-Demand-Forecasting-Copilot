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

| Stage                     | Status   |
| ------------------------- | -------- |
| Dataset Construction      | Complete |
| Exploratory Data Analysis | Complete |
| Prophet Forecasting       | Complete |
| XGBoost Forecasting       | Complete |

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

* Production dataset construction pipeline
* Centralized project configuration
* Modular Prophet forecasting package
* Modular XGBoost forecasting package
* Rolling time-series cross-validation
* Holdout forecasting evaluation
* Forecast performance metrics
* Forecast visualization
* Automatic forecast export
* Production-ready documentation

---

# Technology Stack

## Programming

* Python

## Data Engineering

* Pandas
* DuckDB

## Forecasting

* Prophet
* XGBoost

## Artificial Intelligence

* Google Gemini
* LangChain

## Vector Database

* ChromaDB

## Embeddings

* Sentence Transformers
* all-MiniLM-L6-v2

## Frontend

* Streamlit

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


---

# Prerequisites

Before running the project, ensure the following are installed:

* Python 3.11 or later
* Git

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

* `train.csv`
* `items.csv`

---

# Running the Project

From the project root, run:

```bash
python src/main.py
```

The production pipeline will automatically execute the following stages:

1. Dataset Construction
2. Prophet Forecasting
3. XGBoost Forecasting

The console displays forecasting progress, cross-validation metrics, holdout evaluation metrics, and generates forecast visualizations.

---

# Generated Outputs

Running the project automatically creates:

* Processed category sales dataset
* Prophet holdout predictions
* Prophet cross-validation metrics
* XGBoost holdout predictions
* XGBoost cross-validation metrics

Generated files are stored under the project's `data/` directory.



# Documentation

Project documentation is available under:

```
docs/
```

Current documentation includes:

* Production stage documentation
* Project architecture

---

# Running the Project

From the project root:

```bash
python src/main.py
```

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

* Inventory Analytics
* Business Metrics
* Retrieval-Augmented Generation (RAG)
* AI Recommendation Engine
* Streamlit Integration

## Future Enhancements

* Logging framework
* Unit testing
* Integration testing
* Continuous Integration (CI)
* Docker support
* Cloud deployment

---

# License

This project is intended for educational and portfolio purposes.
