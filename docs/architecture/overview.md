# Architecture Overview

```mermaid
flowchart LR
  subgraph Customer Space
  A[Customer Admin UI] -- Topics & Sources --> B[Config API]
  A -- Q&A / Trends --> QAPI[Query API]
  A -- Votes (↑/↓) --> FAPI[Feedback API]
  end

  subgraph SaaS Backend (FastAPI)
  B --> CFG[(Postgres: orgs, topics, sources, votes)]
  QAPI --> RAG[LangChain RAG Orchestrator]
  FAPI --> CFG
  end

  subgraph Ingestion
  SRC[RSS/Sitemaps/APIs] --> CRAWL[Fetcher+Parser]
  CRAWL --> ENRICH[Clean, split, embed]
  ENRICH --> VEC[(Chroma: tenant collections)]
  ENRICH --> META[(Postgres: sources, chunks)]
  end

  subgraph Jobs
  SCHED[Scheduler (Celery/Arq)]
  SCHED -- 30-120m --> CRAWL
  SCHED -- 09:00 IST --> DIG[Daily Digest Builder]
  DIG --> RAG
  RAG --> VEC
  RAG --> META
  DIG --> DD[(Postgres: digests)]
  end

  subgraph Realtime
  QAPI --> RTAGG[Realtime Trend Aggregator]
  RTAGG --> REDIS[(Redis: windows)]
  REDIS --> QAPI
```
