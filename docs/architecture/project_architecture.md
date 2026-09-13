# Project Architecture

## 1. Overview

The AI Retail Demand Forecasting Copilot follows a modular production architecture.

The project follows an **experiment-first, production-second** workflow. Experimental work is developed and validated before the relevant functionality is organized into reusable production components.

The architecture has evolved in two phases:

1. **Original ML application — Stage 01 through Stage 09**
2. **Post-Stage 9 production engineering and MLOps enhancements**

Stage 09 completed the original end-to-end ML application. The work after Stage 09 extends that application with engineering and serving capabilities without changing the original project history.

---

## 2. Original Production Architecture

The original production application was centered around the Streamlit application.

```text
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

This represents the original production ML application completed through Stage 09.

---

## 3. Original Production Components

### Dataset Construction

Responsible for building the processed retail dataset used by the forecasting pipeline.

### Demand Forecasting

The forecasting layer contains:

- Prophet
- XGBoost

The forecasting pipelines operate on retail store-category time series.

### Inventory Analytics

Calculates inventory-oriented outputs including:

- Projected inventory
- Inventory gap
- Stockout risk
- Overstock risk
- Risk severity

The main analysis object is:

```text
InventoryAnalysis
```

### Business Metrics

Transforms forecasting and inventory results into business-oriented metrics.

The main analysis object is:

```text
BusinessAnalysis
```

Examples include:

- Potential lost sales
- Revenue risk
- Inventory at risk
- Recommended order quantity
- Inventory health score

### Retrieval-Augmented Generation (RAG)

Retrieves relevant business knowledge from the inventory knowledge base using semantic search.

### AI Recommendation Engine

Combines:

- Inventory analysis
- Business analysis
- Retrieved knowledge
- User instructions

to generate a structured recommendation containing:

```text
Recommendation
├── summary
├── recommendation
└── rationale
```

### Streamlit Application

The original Streamlit application provided the production user interface and orchestrated the production workflow.

The Stage 09 design intentionally performed the forecasting analysis once and reused the resulting analysis for multiple recommendation requests.

---

## 4. Original Source Structure

The original production structure was organized around `app.py` and the reusable `src` packages.

```text
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

The detailed Stage 09 Streamlit implementation is documented separately in:

```text
docs/stages/stage_09_streamlit.md
```

---

## 5. Architectural Evolution After Stage 09

Stage 09 represents the completion of the original end-to-end ML application.

After Stage 09, the project entered a separate phase:

**Post-Stage 9 — Production Engineering & MLOps Enhancements**

The purpose of this phase is to add engineering capabilities around the completed ML application.

```text
Original ML Application
        |
        v
Stage 09 — Streamlit Application
        |
        v
Original Project Complete
        |
        v
Post-Stage 9
        |
        +-- 9A — Automated Testing & CI
        |
        +-- 9B — FastAPI Model Serving
        |
        +-- 9C — Docker Containerization
        |
        +-- 9D — Kubernetes Deployment
        |
        +-- 9E — MLflow Tracking
        |
        +-- 9F — Monitoring & Observability
```

Only the first two post-Stage 9 enhancements are currently complete.

---

## 6. Current Production Architecture

The major architectural change after Stage 09 is the introduction of a FastAPI backend between the Streamlit UI and the production application services.

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

Streamlit remains the user-facing presentation layer.

FastAPI provides the backend service boundary.

The existing forecasting, inventory, business metrics, RAG, and recommendation components remain part of the production application.

---

## 7. Current Production Request Flow

The current application workflow is:

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

The original user experience is preserved while the backend processing is now exposed through FastAPI.

---

## 8. FastAPI Service Boundary

FastAPI provides a defined service interface for the production application.

Current endpoints:

```text
GET  /health
GET  /ready
POST /predict
POST /recommend
```

### `/health`

Provides a basic service health check.

### `/ready`

Provides a readiness check for the API service.

### `/predict`

Accepts a selected store and category and executes the forecasting and downstream inventory/business analysis workflow.

### `/recommend`

Generates an AI recommendation using the latest analysis results.

The latest analysis is retained in application memory for local operation so multiple recommendation requests can be made without rerunning the forecasting pipeline.

---

## 9. Forecasting Service Boundary

The forecasting workflow was moved behind a reusable application-level service boundary rather than being duplicated inside the API layer.

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

The API layer uses this service instead of duplicating the forecasting and business logic.

### Forecasting Scope

The retail dataset contains multiple store-category time series.

For the local implementation, forecasting is scoped to a selected store and category rather than attempting to forecast every series simultaneously. This keeps local training and inference computationally manageable while providing a clear API boundary for future scaling.

---

## 10. API Request and Response Contracts

The FastAPI layer uses Pydantic schemas to define request and response structures.

Conceptually, the API contains:

```text
PredictionRequest
PredictionResponse

RecommendationRequest
RecommendationResponse
```

This establishes a defined contract between the Streamlit frontend and FastAPI backend.

---

## 11. Current Source Structure

The current production structure extends the original structure with the API and service layers.

```text
app.py

api/
├── main.py
└── schemas.py

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
├── services/
│   └── demand_forecasting_service.py
├── config.py
└── main.py

tests/
└── test_inventory.py
```

The architectural responsibilities are now separated as follows:

- `experiments/` — experimentation and development
- `src/` — reusable production ML and business logic
- `api/` — backend API and request/response contracts
- `app.py` — Streamlit presentation layer
- `tests/` — automated tests

---

## 12. Automated Testing and CI Architecture

Automated testing was introduced after Stage 09 as the first production engineering enhancement.

A deterministic inventory unit test validates production inventory position calculations.

GitHub Actions runs the configured test in a clean Python environment.

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

The current CI workflow focuses on the targeted inventory test rather than running the full forecasting pipeline.

---

## 13. Design Principles

The production architecture follows these principles:

- Modular architecture
- Separation of concerns
- Single Responsibility Principle
- Experiment before production
- Configuration over hardcoding
- Reusable production components
- Lightweight automated testing
- Clear API boundaries
- Incremental productionization

The architecture intentionally avoids introducing infrastructure complexity before it provides practical value.

---

## 14. Current Enhancement Status

| Capability | Status |
|---|---|
| Original ML application | Complete |
| Stage 09 — Streamlit Application | Complete |
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

## 15. Production Engineering Roadmap

The post-Stage 9 architecture is intended to evolve incrementally.

```text
9A — Automated Testing & CI
              ✓
              |
              v
9B — FastAPI Model Serving
              ✓
              |
              v
9C — Docker Containerization
              |
              v
9D — Kubernetes Deployment
              |
              v
9E — MLflow Tracking
              |
              v
9F — Monitoring & Observability
```

Future engineering work may also include automated deployment/CD, container security scanning, autoscaling, container registry integration, or simple cloud deployment where appropriate.

These future capabilities are not currently part of the completed architecture.
