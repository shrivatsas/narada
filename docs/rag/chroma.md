# Chroma Store

- One collection per user: `user_{user_id}` for simple isolation.
- IDs: `${document_id}:${chunk_index}`
- Metadatas: `{ user_id, document_id, source_id, url, published_at, tags }`
- Documents: chunk text
- Embeddings: start with a small, fast model (e.g., `intfloat/e5-small-v2`), keep swappable.
