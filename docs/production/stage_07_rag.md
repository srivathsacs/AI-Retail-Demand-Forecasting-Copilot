# Stage 07 — Retrieval-Augmented Generation (RAG)

## Overview

Stage 7 introduces Retrieval-Augmented Generation (RAG) into the AI Retail Demand Forecasting Copilot.

The objective of this stage is to build a production-ready retrieval layer capable of searching an inventory knowledge base using semantic search.

Unlike the experimental implementation, the production design separates knowledge retrieval from recommendation generation.

This stage is responsible only for retrieving relevant business knowledge. Recommendation generation and prompt engineering are implemented in the next stage.

---

# Objectives

- Load knowledge base documents
- Split documents into semantic chunks
- Generate vector embeddings
- Store embeddings in a Chroma vector database
- Retrieve the most relevant knowledge for downstream stages
- Provide a reusable retrieval interface

---

# Production Architecture

```
Knowledge Base
        │
        ▼
Document Loader
        │
        ▼
Chunker
        │
        ▼
Vector Store (Chroma)
        │
        ▼
Retriever
        │
        ▼
KnowledgeRetriever
```

---

# Production Package

```
src/
└── rag/
    ├── __init__.py
    ├── chunker.py
    ├── document_loader.py
    ├── indexer.py
    ├── knowledge_retriever.py
    ├── retriever.py
    └── vector_store.py
```

---

# Module Responsibilities

## document_loader.py

Loads Markdown documents from the knowledge base.

---

## chunker.py

Splits Markdown documents into semantic chunks using level-2 Markdown headings.

---

## vector_store.py

Responsible for:

- generating embeddings
- managing the Chroma database
- indexing document chunks

---

## retriever.py

Performs semantic similarity search against the vector database.

Returns structured retrieval results.

---

## knowledge_retriever.py

Provides a simple production interface for retrieving relevant knowledge.

Downstream stages interact with this module instead of Chroma directly.

---

## indexer.py

Builds or updates the vector database from the knowledge base.

Indexing is separated from retrieval to avoid rebuilding embeddings during normal application execution.

---

# Design Decisions

The production implementation intentionally differs from the experimental implementation.

The experiment combined:

- document loading
- chunking
- embedding generation
- vector storage
- retrieval
- prompt construction
- Gemini interaction

into a small number of scripts.

The production implementation separates these responsibilities into reusable modules following the Single Responsibility Principle.

---

# Stage Output

Stage 7 returns retrieved knowledge that can be consumed by downstream stages.

It does not generate recommendations.

---

# Integration

Current production pipeline:

```
Forecast
        ↓
InventoryAnalysis
        ↓
BusinessAnalysis
        ↓
Knowledge Retrieval
```

The Recommendation Engine consumes the retrieved knowledge in the next production stage.

---

# Validation

Stage 7 was validated by verifying:

- document loading
- Markdown chunking
- embedding generation
- Chroma indexing
- semantic retrieval
- integration with the production repository

The Stage 1–6 production pipeline was also revalidated to ensure the Stage 7 migration introduced no regressions.

---

# Stage Status

**Completed**

Production migration finalized.