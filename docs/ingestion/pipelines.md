# Ingestion and Pipelines

Ingestion & indexing
1. Fetch new items from enabled sources for a user.
2. Normalize → clean HTML → detect language → semantic chunk (500–800 tokens, ~80 overlap).
3. Embed → upsert into Chroma collection `user_{user_id}` with metadata.
4. Insert documents and chunks into Postgres; dedupe on `hash(url+content)`.

Retrieval & summarization (LangChain)
- Retriever: Chroma with `k=12`, filter: `{ "published_at": { "$gte": now-30d } }`.
- Optional reranker (cross-encoder) to boost quality.
- Chain: condense query → retrieve → rerank → map-reduce summarize into bullets with citations.

Daily digest (09:00 IST)
- For each user: take last 24h docs, score by recency + source priority + tag prefs.
- Dedupe near-duplicates (cosine similarity).
- Generate 5–7 bullets with links; store in `digests`, notify (email/webhook).

At-the-moment trendline (realtime)
- Redis keeps time-bucketed counters per user: keys like `trend:{user_id}:{tag}:{bucket_ts}`.
- Increment on ingestion (extracted tags/entities), user queries, and votes.
- Trendline = EMA/WMA across last N buckets; return top rising tags with sparkline.
