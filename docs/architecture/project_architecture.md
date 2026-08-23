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
                     Forecast Output Files
                                 |
                                 v
                  +-------------------------------+
                  | Inventory Analytics           |
                  +---------------+---------------+
                                  |
                                  v
                  +-------------------------------+
                  | InventoryAnalysis             |
                  +---------------+---------------+
                                  |
                                  v
                  +-------------------------------+
                  | Business Metrics              |
                  +---------------+---------------+
                                  |
                                  v
                  +-------------------------------+
                  | BusinessAnalysis              |
                  +---------------+---------------+
                                  |
                                  v
                  +-------------------------------+
                  | Knowledge Retrieval (RAG)     |
                  +---------------+---------------+
                                  |
                                  v
                  +-------------------------------+
                  | Recommendation Engine         |
                  +---------------+---------------+
                                  |
                                  v
                  +-------------------------------+
                  | Recommendation                |
                  +-------------------------------+
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
│   ├── __init__.py
│   ├── inventory_analysis.py
│   ├── inventory_position.py
│   └── risk_engine.py
│
├── metrics/
│   ├── __init__.py
│   ├── business_analysis.py
│   └── business_metrics.py
│
├── rag/
│   ├── __init__.py
│   ├── chunker.py
│   ├── document_loader.py
│   ├── indexer.py
│   ├── knowledge_retriever.py
│   ├── retriever.py
│   └── vector_store.py
│
├── recommendation/
│   ├── __init__.py
│   ├── prompt_builder.py
│   ├── recommendation.py
│   └── recommendation_engine.py
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

# Inventory Analytics Package Design

```
inventory/
├── inventory_analysis.py
├── inventory_position.py
└── risk_engine.py
```

## Responsibilities

### inventory_position.py

Calculates projected inventory and inventory gap.

---

### risk_engine.py

Evaluates stockout risk, overstock risk, and overall inventory risk severity.

---

### inventory_analysis.py

Represents the reusable output of the Inventory Analytics stage for downstream consumers.

---

# Business Metrics Package Design

```
metrics/
├── business_analysis.py
└── business_metrics.py
```

## Responsibilities

### business_metrics.py

Calculates business metrics from inventory analysis.

---

### business_analysis.py

Represents the reusable output of the Business Metrics stage for downstream consumers.

---

# Retrieval-Augmented Generation Package Design

```
rag/
├── document_loader.py
├── chunker.py
├── vector_store.py
├── retriever.py
├── knowledge_retriever.py
└── indexer.py
```

## Responsibilities

### document_loader.py

Loads Markdown documents from the knowledge base.

---

### chunker.py

Splits Markdown documents into semantic chunks.

---

### vector_store.py

Generates embeddings and manages the Chroma vector database.

---

### retriever.py

Performs semantic similarity search.

---

### knowledge_retriever.py

Provides a production interface for retrieving relevant knowledge.

---

### indexer.py

Builds and updates the vector database from the knowledge base.

---

# Recommendation Engine Package Design

```
recommendation/
├── recommendation.py
├── prompt_builder.py
└── recommendation_engine.py
```

## Responsibilities

### recommendation.py

Represents the reusable recommendation output for downstream consumers.

---

### prompt_builder.py

Builds the final prompt from business analysis and retrieved knowledge.

---

### recommendation_engine.py

Coordinates knowledge retrieval, prompt generation, Gemini interaction, and returns a structured `Recommendation`.

---

# Configuration

All project configuration is centralized in:

```
src/config.py
```

Configuration includes:

- File paths
- Forecast settings
- Inventory settings
- Business metrics settings
- RAG settings
- Recommendation settings
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
| XGBoost Forecasting | Complete |
| Inventory Analytics | Complete |
| Business Metrics | Complete |
| Retrieval-Augmented Generation (RAG) | Complete |
| AI Recommendation Engine | Complete |

---

# Future Architecture

The following module remains to be integrated:

- Streamlit Application