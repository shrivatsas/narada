# Data Model

Users
- `id` (pk), `email` (unique), `password_hash`, `plan`, `created_at`

Sources
- `id` (pk), `user_id` (fk→users.id), `type` (rss|site|api), `url`, `tags` (jsonb),
  `crawl_interval_m` (int), `enabled` (bool), `last_crawled_at`

Documents
- `id` (pk), `user_id`, `source_id` (fk), `url`, `title`, `author`,
  `published_at` (timestamptz), `ingested_at`, `hash` (dedupe), `status` (new|embedded|error),
  `lang`, `tags` (jsonb)

Chunks
- `id` (pk), `user_id`, `document_id` (fk), `chunk_index` (int), `text` (text), `token_count` (int),
  `embedding_ref` (string id in Chroma), `metadata_json` (jsonb)

Digests
- `id` (pk), `user_id`, `date_utc`, `headline` (text), `bullets_json` (jsonb), `model` (text), `created_at`
  - Bullet shape: `{ "text": "...", "doc_ids": [...], "urls": [...], "tags": [...] }`

Votes
- `id` (pk), `user_id`, `target_type` (digest_bullet|doc|answer_snippet), `target_id` (uuid or composite),
  `vote` (int in {-1, 0, 1}), `created_at`

Queries
- `id` (pk), `user_id`, `query_text` (text), `created_at`

Preferences (optional)
- `id` (pk), `user_id`, `tag` (text), `weight` (float), `updated_at`

Trends (optional snapshots)
- `id` (pk), `user_id`, `metric` (tag_count), `time_window` (15m|1h|24h), `tag` (text), `value` (float), `computed_at`
