# AI Retail Demand Forecasting Copilot

## Overview

AI Retail Demand Forecasting Copilot is an end-to-end AI decision-support system for retail inventory planning.

The project combines:

- Retail demand forecasting
- Inventory analytics
- Business metrics
- Retrieval-Augmented Generation (RAG)
- Generative AI recommendations
- Streamlit
- FastAPI
- Automated testing
- GitHub Actions CI

The system is designed to move from historical retail data to demand forecasts, inventory risk analysis, and actionable business recommendations.

The project follows an **experiment-first, production-second** workflow:

1. Develop and validate ideas in `experiments/`.
2. Migrate stable functionality into reusable production code under `src/`.
3. Expose production capabilities through application services and APIs.
4. Document the architecture and implementation.
5. Add production engineering and MLOps capabilities incrementally.

---

# Project Journey

The project is intentionally divided into two phases.

```text
============================================================
PHASE 1 — ORIGINAL ML APPLICATION
============================================================

Stage 01
   |
   v
Stage 02
   |
   v
...
   |
   v
Stage 09 — Streamlit Application
   |
   v
ORIGINAL ML APPLICATION COMPLETE


============================================================
PHASE 2 — PRODUCTION ENGINEERING & MLOps
============================================================

9A — Automated Testing & CI          Complete
   |
   v
9B — FastAPI Model Serving           Complete
   |
   v
9C — Docker Containerization         Planned
   |
   v
9D — Kubernetes Deployment           Planned
   |
   v
9E — MLflow Tracking                 Planned
   |
   v
9F — Monitoring & Observability      Planned
```

The second phase extends the completed ML application. It does not change the original Stage 01–09 project history.

---

# Original System Architecture

The original production application was built around the Streamlit interface.

```text
Raw Retail Data
      |
      v
Dataset Construction
      |
      v
Processed Sales Dataset
      |
      v
Demand Forecasting
  +----------------+
  | Prophet        |
  | XGBoost        |
  +----------------+
      |
      v
Inventory Analytics
      |
      v
Business Metrics
      |
      v
Knowledge Retrieval (RAG)
      |
      v
AI Recommendation Engine
      |
      v
Streamlit Application
```

Stage 09 completed this original end-to-end ML application.

The Streamlit application allowed the user to run the forecasting analysis once and then generate multiple AI recommendations without rerunning the expensive forecasting workflow.

---

# Current Production Architecture

Following Stage 09, the application has been extended with a FastAPI backend.

```text
                         User
                           |
                           v
                +-----------------------+
                | Streamlit Application |
                +-----------+-----------+
                            |
                           HTTP
                            |
                            v
                +-----------------------+
                |    FastAPI Backend    |
                +-----------+-----------+
                            |
             +--------------+--------------+
             |              |              |
             v              v              v
        Forecasting   Inventory Logic   AI Recommendation
        Prophet/XGB                     Gemini + RAG
```

The architectural responsibilities are now separated:

- **Streamlit** — user interface and presentation
- **FastAPI** — backend API/service boundary
- **`src/`** — production ML and business logic
- **`tests/`** — automated tests
- **`experiments/`** — experimentation and development

The existing forecasting, inventory, business metrics, RAG, and recommendation components remain part of the production application.

Detailed architecture documentation is available in:

```text
docs/architecture/project_architecture.md
```

---

# Core Capabilities

## Demand Forecasting

The project uses two forecasting approaches:

- Prophet
- XGBoost

The forecasting workflow includes:

- Time-series feature preparation
- Rolling time-series cross-validation
- Holdout evaluation
- Forecast performance metrics
- Forecast visualization
- Forecast export

The local production workflow is scoped to a selected store and category rather than attempting to forecast every store-category time series simultaneously.

---

## Inventory Analytics

Forecast demand is translated into inventory-oriented decision metrics.

The inventory layer calculates:

- Projected inventory
- Inventory gap
- Stockout risk
- Overstock risk
- Risk severity

The main structured output is:

```text
InventoryAnalysis
```

---

## Business Metrics

Inventory analysis is converted into business-oriented measures.

Examples include:

- Potential lost sales
- Revenue risk
- Inventory at risk
- Recommended order quantity
- Inventory health score

The main structured output is:

```text
BusinessAnalysis
```

---

## Retrieval-Augmented Generation

The recommendation workflow uses a knowledge base to retrieve relevant business context.

The RAG layer includes:

- Knowledge base document loading
- Semantic document chunking
- Sentence Transformer embeddings
- Chroma vector database
- Semantic retrieval

---

## AI Recommendations

The recommendation engine combines:

- Inventory analysis
- Business analysis
- Retrieved knowledge
- Optional user instructions

Google Gemini generates a structured recommendation containing:

```text
Recommendation
├── summary
├── recommendation
└── rationale
```

---

# Post-Stage 9 Production Engineering

## 9A — Automated Testing & CI

### Status: Complete

A deterministic unit test was added for the production inventory calculation.

The current test validates inventory position behavior using controlled inputs rather than running the full forecasting pipeline.

Test location:

```text
tests/test_inventory.py
```

GitHub Actions provides continuous integration.

```text
Code Change
    |
    v
GitHub Repository
    |
    v
GitHub Actions
    |
    v
Clean Ubuntu Runner
    |
    v
Python 3.11
    |
    v
Install Dependencies
    |
    v
Run Pytest
    |
    v
PASS / FAIL
```

The current CI workflow runs the targeted inventory test.

Workflow location:

```text
.github/workflows/ci.yml
```

CI is intentionally lightweight because the full forecasting workflow uses a large dataset and computationally heavier ML components.

---

## 9B — FastAPI Model Serving

### Status: Complete

FastAPI was introduced as a backend API layer between Streamlit and the production services.

Backend location:

```text
api/
├── main.py
└── schemas.py
```

The API currently exposes:

```text
GET  /health
GET  /ready
POST /predict
POST /recommend
```

### Health

`/health` confirms that the API service is running.

### Readiness

`/ready` provides a readiness check for the service.

### Prediction

`/predict` accepts:

```text
store_id
category
```

and executes:

```text
Dataset Construction
        |
        v
Prophet Forecasting
        |
        v
XGBoost Forecasting
        |
        v
Inventory Analytics
        |
        v
Business Metrics
```

The API returns structured inventory and business analysis.

### Recommendation

`/recommend` generates an AI recommendation using the latest analysis.

The latest analysis is reused so that multiple recommendation requests do not rerun the forecasting pipeline.

---

# Streamlit → FastAPI Integration

### Status: Complete

The original Streamlit user experience has been preserved while the backend processing has been separated into FastAPI.

Current workflow:

```text
Run Analysis
      |
      v
Streamlit
      |
      | HTTP
      v
FastAPI /predict
      |
      v
Forecasting + Inventory + Business Analysis
      |
      v
Display Analysis
      |
      v
Generate Recommendation
      |
      | HTTP
      v
FastAPI /recommend
      |
      v
Gemini + RAG
      |
      v
Display Recommendation
```

This creates a clear separation between presentation and backend services without changing the underlying forecasting and business logic.

---

# Demand Forecasting Service

A reusable application-level service was introduced to provide a single service boundary for the forecasting and downstream business workflow.

Location:

```text
src/services/demand_forecasting_service.py
```

The service accepts:

```text
store_id
category
```

and returns:

```text
InventoryAnalysis
BusinessAnalysis
```

The FastAPI backend uses this service rather than duplicating forecasting and business logic inside the API layer.

---

# API Contracts

FastAPI uses Pydantic schemas for request and response validation.

Current request/response models include:

```text
PredictionRequest
PredictionResponse

RecommendationRequest
RecommendationResponse
```

This creates a defined interface between the Streamlit frontend and FastAPI backend.

---

# Current Production Structure

```text
AI-Retail-Demand-Forecasting-Copilot/
│
├── app.py
│
├── api/
│   ├── main.py
│   └── schemas.py
│
├── src/
│   ├── analysis/
│   ├── data/
│   ├── features/
│   ├── forecasting/
│   │   ├── prophet/
│   │   └── xgboost/
│   ├── inventory/
│   ├── metrics/
│   ├── rag/
│   ├── recommendation/
│   ├── services/
│   │   └── demand_forecasting_service.py
│   ├── config.py
│   └── main.py
│
├── experiments/
│
├── tests/
│   └── test_inventory.py
│
├── data/
│   └── raw/
│
├── docs/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── requirements.txt
└── README.md
```

---

# Technology Stack

| Area | Technology |
|---|---|
| Language | Python 3.11 |
| Data Processing | Pandas |
| Data Engineering | DuckDB |
| Forecasting | Prophet |
| Forecasting | XGBoost |
| Generative AI | Google Gemini |
| RAG | LangChain |
| Vector Database | ChromaDB |
| Embeddings | Sentence Transformers |
| Frontend | Streamlit |
| Backend API | FastAPI |
| API Server | Uvicorn |
| Validation | Pydantic |
| Testing | pytest |
| Continuous Integration | GitHub Actions |
| Version Control | Git / GitHub |

---

# Dataset

This project uses the **Corporación Favorita Grocery Sales Forecasting** dataset from Kaggle.

The complete raw dataset is not included in the repository.

Place the required CSV files under:

```text
data/raw/
```

The repository's raw data directory contains the project datasets used by the production pipeline, including:

```text
holidays_events.csv
items.csv
oil.csv
stores.csv
test.csv
train.csv
transactions.csv
```

The training dataset is large, so the local forecasting workflow is intentionally scoped to a selected store and category.

---

# Prerequisites

Before running the project, install:

- Python 3.11 or later
- Git

A virtual environment is recommended.

---

# Installation

Clone the repository:

```bash
git clone https://github.com/srivathsacs/AI-Retail-Demand-Forecasting-Copilot.git
cd AI-Retail-Demand-Forecasting-Copilot
```

Create a virtual environment:

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Environment Variables

The recommendation engine uses Google Gemini.

Create a `.env` file in the project root:

```text
GOOGLE_API_KEY=your_api_key_here
```

Do not commit the `.env` file or expose the API key.

---

# Running the Production Pipeline

The command-line production entry point is:

```bash
python src/main.py
```

The production pipeline covers:

1. Dataset Construction
2. Prophet Forecasting
3. XGBoost Forecasting
4. Inventory Analytics
5. Business Metrics
6. Retrieval-Augmented Generation
7. AI Recommendation Engine

---

# Running the FastAPI Backend

Start the API server:

```bash
uvicorn api.main:app --reload
```

The API is available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

Health endpoint:

```text
http://127.0.0.1:8000/health
```

Readiness endpoint:

```text
http://127.0.0.1:8000/ready
```

---

# Running the Streamlit Application

Start Streamlit:

```bash
streamlit run app.py
```

The application is available at:

```text
http://localhost:8501
```

The current Streamlit application communicates with the FastAPI backend.

For the integrated application, start FastAPI first and then start Streamlit.

---

# Testing

The project includes an automated inventory unit test.

Set the production source directory on Windows PowerShell:

```powershell
$env:PYTHONPATH="src"
```

Run the targeted test:

```powershell
pytest tests\test_inventory.py
```

GitHub Actions runs the same targeted test automatically for pushes to `main` and pull requests targeting `main`.

The current CI scope is intentionally focused on deterministic production logic rather than running the full forecasting pipeline against the large retail dataset.

---

# Validation Performed

The production application and post-Stage 9 enhancements have been validated incrementally.

The current validation includes:

- Streamlit application startup
- End-to-end forecasting workflow
- Inventory analysis
- Business analysis
- Gemini recommendation generation
- Multiple recommendation requests without rerunning forecasting
- FastAPI health endpoint
- FastAPI readiness endpoint
- FastAPI prediction endpoint
- FastAPI recommendation endpoint
- Streamlit → FastAPI integration
- Inventory unit test
- GitHub Actions CI execution

---

# Generated Outputs

Running the forecasting workflow can generate outputs such as:

- Processed category sales dataset
- Prophet holdout predictions
- XGBoost holdout predictions
- Forecast metrics
- Inventory analysis
- Business metrics
- Knowledge-base/vector-store data
- AI-generated recommendations

Generated artifacts should remain local and should not be committed unless they are intentionally part of the project.

---

# Documentation

Project documentation is available under:

```text
docs/
```

Important documentation includes:

```text
docs/
├── architecture/
│   └── project_architecture.md
└── stages/
    └── stage_09_streamlit.md
```

### Stage 09

`stage_09_streamlit.md` documents the original production Streamlit application and its workflow.

### Project Architecture

`project_architecture.md` documents:

- Original architecture
- Current architecture
- Architectural evolution
- Production component boundaries
- FastAPI service boundary
- Source structure
- CI architecture
- Production engineering roadmap

---

# Current Project Status

| Capability | Status |
|---|---|
| Dataset Construction | Complete |
| Exploratory Data Analysis | Complete |
| Prophet Forecasting | Complete |
| XGBoost Forecasting | Complete |
| Inventory Analytics | Complete |
| Business Metrics | Complete |
| Retrieval-Augmented Generation | Complete |
| AI Recommendation Engine | Complete |
| Stage 09 Streamlit Application | Complete |
| Automated Inventory Test | Complete |
| GitHub Actions CI | Complete |
| FastAPI Backend | Complete |
| Health Endpoint | Complete |
| Readiness Endpoint | Complete |
| Forecasting API | Complete |
| Recommendation API | Complete |
| Streamlit → FastAPI Integration | Complete |
| Docker Containerization | Planned |
| Kubernetes Deployment | Planned |
| MLflow Tracking | Planned |
| Monitoring & Observability | Planned |
| Automated Deployment / CD | Planned |

---

# Production Engineering Roadmap

## 9C — Docker Containerization

**Status: Planned**

Planned focus:

- Dockerfile
- Reproducible application image
- Local container execution
- Container health checks

---

## 9D — Kubernetes Deployment

**Status: Planned**

The current direction is to use a local Kubernetes environment such as `kind` before considering cloud deployment.

Planned focus:

- Kubernetes Deployment
- Kubernetes Service
- Configuration
- Health probes
- Readiness probes
- Local deployment

---

## 9E — MLflow Tracking

**Status: Planned**

Planned focus:

- Experiment tracking
- Model metrics
- Model artifacts
- Model versioning

---

## 9F — Monitoring & Observability

**Status: Planned**

Planned focus:

- Application logging
- API request monitoring
- Health monitoring
- Basic model-serving metrics

Prometheus/Grafana may be considered later if they provide clear value.

---

## Future Deployment

Automated deployment/CD is currently planned but not implemented.

Potential future extensions include:

- Automated deployment
- Container registry integration
- Container security scanning
- Kubernetes autoscaling
- Simple cloud deployment

These are future engineering enhancements and are not represented as completed capabilities.

---

# Design Principles

The project follows these practical principles:

- **Experiment before production**
- **Separation of concerns**
- **Reusable production components**
- **Configuration over hardcoding**
- **Clear API boundaries**
- **Lightweight automated testing**
- **Incremental productionization**
- **Avoid unnecessary infrastructure complexity**

The goal is to demonstrate a realistic progression from an ML application to a production-oriented ML system rather than introducing infrastructure purely for technology's sake.

---

# Portfolio / Interview Summary

This project demonstrates the progression from an end-to-end machine learning application to a more production-oriented ML system.

The original application covers:

```text
Retail Data
    ↓
Demand Forecasting
    ↓
Inventory Analytics
    ↓
Business Metrics
    ↓
RAG
    ↓
Generative AI Recommendations
    ↓
Streamlit
```

The production engineering extension adds:

```text
Automated Testing
        ↓
GitHub Actions CI
        ↓
FastAPI Model Serving
        ↓
Streamlit → API Integration
        ↓
Docker
        ↓
Kubernetes
        ↓
MLflow
        ↓
Monitoring
```

The first two post-Stage 9 engineering layers are complete today: **automated testing/CI and FastAPI model serving**. The remaining infrastructure and MLOps layers are planned as the next development stages.

---

# License

This project is intended for educational and portfolio purposes.
