# AI Retail Demand Forecasting Copilot

## Overview

AI Retail Demand Forecasting Copilot is an end-to-end AI decision support system for retail inventory planning.

The project combines demand forecasting, inventory analytics, Retrieval-Augmented Generation (RAG), Generative AI, and an interactive Streamlit application to help retailers make better inventory decisions.

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
| Business Metrics | Complete |
| Retrieval-Augmented Generation (RAG) | Complete |
| AI Recommendation Engine | Complete |
| Streamlit Application | Complete |

---

# Current Production Structure

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

# Current Features

- Production dataset construction pipeline
- Centralized project configuration
- Modular Prophet forecasting package
- Modular XGBoost forecasting package
- Production Inventory Analytics package
- Production Business Metrics package
- Production Retrieval-Augmented Generation package
- Production AI Recommendation Engine
- Interactive Streamlit application
- Knowledge base document loading
- Semantic document chunking
- Chroma vector database integration
- Sentence Transformer embeddings
- Semantic knowledge retrieval
- Prompt builder for AI recommendations
- Google Gemini integration
- Structured AI recommendation output
- Session-based recommendation workflow
- Inventory position calculation
- Inventory risk assessment
- Business metrics calculation
- Structured inventory analysis output
- Structured business analysis output
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
app.py
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

# Environment Variables

This stage uses **Google Gemini** for AI recommendation generation.

Create a `.env` file in the project root:

```text
GOOGLE_API_KEY=your_api_key_here
```

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

## Command-line Pipeline

Run the complete production pipeline from the command line:

```bash
python src/main.py
```

The command-line pipeline executes:

1. Dataset Construction
2. Prophet Forecasting
3. XGBoost Forecasting
4. Inventory Analytics
5. Business Metrics
6. Retrieval-Augmented Generation (RAG)
7. AI Recommendation Engine

The console displays:

- Cross-validation metrics
- Holdout evaluation metrics
- Inventory analytics
- Business metrics
- Retrieved knowledge
- AI-generated executive summary
- AI recommendations
- Business rationale

Forecast visualizations are generated automatically during execution.

---

## Streamlit Application

Launch the interactive web application:

```bash
streamlit run app.py
```

The Streamlit application provides:

- Interactive inventory decision-support dashboard
- One-click execution of the complete forecasting pipeline
- Current Analysis dashboard
- AI-powered inventory recommendations
- Custom recommendation prompts
- Multiple recommendation generation without rerunning forecasting
- Session-based workflow for improved responsiveness

---

# Generated Outputs

Running the project automatically creates:

- Processed category sales dataset
- Prophet holdout predictions
- Prophet cross-validation metrics
- XGBoost holdout predictions
- XGBoost cross-validation metrics
- Inventory analytics results
- Business metrics results
- Chroma vector database
- Indexed knowledge base
- AI-generated recommendations

Generated files are stored locally under the project's `data/` directory and `chroma_db/`.

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

## Current Status

The complete production application has been implemented.

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
