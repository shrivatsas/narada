# Feedback Loop

- Write to `votes(user_id, target_type, target_id, vote)`.
- Maintain preferences:
  - `weight(tag) = clip(μ + α*upvotes − β*downvotes, bounds)`
- Apply at:
  - Retrieval: `final_score = sim + λ * sum(tag_weights)` (or pass as features to reranker)
  - Digest selection: down-weight disliked tags/sources; up-weight liked ones.
