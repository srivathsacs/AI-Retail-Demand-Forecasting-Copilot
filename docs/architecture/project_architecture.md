# Project Architecture

## Overview

The AI Retail Demand Forecasting Copilot follows a modular production architecture.

Each business capability is implemented as an independent package with a single responsibility.

The project follows an **experiment-first, production-second** workflow, where every completed experiment is gradually migrated into production-quality code.

---

# Production System Architecture

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
                  | AI Recommendation Engine      |
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
                        User
                          │
                          ▼
               +-----------------------+
               | Streamlit Application |
               +-----------+-----------+
                           │
                Run Analysis│
                           ▼
            +----------------------------+
            | Dataset Construction       |
            +-------------+--------------+
                          │
                          ▼
            +----------------------------+
            | Prophet Forecasting        |
            +-------------+--------------+
                          │
                          ▼
            +----------------------------+
            | XGBoost Forecasting        |
            +-------------+--------------+
                          │
                          ▼
            +----------------------------+
            | Inventory Analytics        |
            +-------------+--------------+
                          │
                          ▼
            +----------------------------+
            | Business Metrics           |
            +-------------+--------------+
                          │
                          ▼
              InventoryAnalysis
              BusinessAnalysis
                          │
               (Session State)
                          │
                          ▼
            +----------------------------+
            | AI Recommendation Engine   |
            +-------------+--------------+
                          │
                          ▼
                 Recommendation
                          │
                          ▼
                    Streamlit UI
```

---

# Current Source Structure

```
app.py

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

# Production Packages

## Dataset Construction

Responsible for building the processed retail dataset used throughout the application.

---

## Forecasting

Implements both Prophet and XGBoost forecasting pipelines with validation, evaluation, visualization, and forecast export.

---

## Inventory Analytics

Calculates projected inventory, inventory gap, stockout risk, overstock risk, and overall inventory severity.

Produces:

```
InventoryAnalysis
```

---

## Business Metrics

Transforms inventory analytics into business-ready operational metrics.

Produces:

```
BusinessAnalysis
```

---

## Retrieval-Augmented Generation (RAG)

Indexes the inventory knowledge base and retrieves relevant business knowledge using semantic search.

Produces:

- Retrieved knowledge context

---

## AI Recommendation Engine

Combines:

- InventoryAnalysis
- BusinessAnalysis
- Retrieved knowledge

to generate structured AI recommendations using Google Gemini.

Produces:

```
Recommendation
├── summary
├── recommendation
└── rationale
```

---

## Streamlit Application

Provides the production user interface.

Responsibilities include:

- Running the forecasting pipeline
- Displaying analysis results
- Managing session state
- Generating multiple AI recommendations without rerunning forecasting

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
| XGBoost Forecasting | Complete |
| Inventory Analytics | Complete |
| Business Metrics | Complete |
| Retrieval-Augmented Generation (RAG) | Complete |
| AI Recommendation Engine | Complete |
| Streamlit Application | Complete |

---

# Project Status

The complete end-to-end production pipeline has been implemented.

Future work will focus on engineering enhancements such as testing, logging, CI/CD, containerization, and cloud deployment.