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
| XGBoost Forecasting | Next Stage |

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
- Time-series cross-validation
- Forecast evaluation
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

# Documentation

Project documentation is available under:

```
docs/
```

Current documentation includes:

- Production stage documentation
- Project architecture

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

- XGBoost Forecasting
- Inventory Analytics
- Business Metrics
- Retrieval-Augmented Generation (RAG)
- AI Recommendation Engine
- Streamlit Integration

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