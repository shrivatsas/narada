# API Design

Auth
- POST `/auth/signup`: `{ email, password }`
- POST `/auth/login`: `{ email, password }`

Sources
- POST `/sources`: `{ type, url, tags?, crawl_interval_m? }`
- GET `/sources`
- PATCH `/sources/{id}`: `{ enabled?, tags?, crawl_interval_m? }`
- DELETE `/sources/{id}`

Digest & Votes
- GET `/digest/today` → `{ headline, bullets: [{ text, urls, tags, id }] }`
- POST `/vote`: `{ target_type, target_id, vote: -1|0|1 }`

Query & Trends
- POST `/query`: `{ q }` → `{ answer, citations: [{ title, url, date }] }`
- GET `/trends?time_window=1h` → `[{ tag, score, points: [t0..tn] }]`

Topic Profile
- POST `/topic-profile`: `{ include_keywords?, exclude_keywords?, entities?, locales?, source_weights? }`
- GET `/topic-profile`
