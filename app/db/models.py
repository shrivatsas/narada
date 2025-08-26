from __future__ import annotations

from datetime import date, datetime
from typing import Any, Literal

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id: int | None = None
    email: EmailStr
    password_hash: str
    plan: str = "free"
    created_at: datetime | None = None


class Source(BaseModel):
    id: int | None = None
    user_id: int
    type: Literal["rss", "site", "api"]
    url: str
    tags: list[str] = Field(default_factory=list)
    crawl_interval_m: int = 60
    enabled: bool = True
    last_crawled_at: datetime | None = None


class Document(BaseModel):
    id: int | None = None
    user_id: int
    source_id: int | None = None
    url: str
    title: str | None = None
    author: str | None = None
    published_at: datetime | None = None
    ingested_at: datetime | None = None
    hash: str | None = None
    status: Literal["new", "embedded", "error"] = "new"
    lang: str | None = None
    tags: list[str] = Field(default_factory=list)


class Chunk(BaseModel):
    id: int | None = None
    user_id: int
    document_id: int
    chunk_index: int
    text: str
    token_count: int | None = None
    embedding_ref: str | None = None
    metadata_json: dict[str, Any] = Field(default_factory=dict)


class DigestBullet(BaseModel):
    text: str
    doc_ids: list[int] = Field(default_factory=list)
    urls: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)


class Digest(BaseModel):
    id: int | None = None
    user_id: int
    date_utc: date
    headline: str | None = None
    bullets_json: list[DigestBullet] = Field(default_factory=list)
    model: str | None = None
    created_at: datetime | None = None


class Vote(BaseModel):
    id: int | None = None
    user_id: int
    target_type: Literal["digest_bullet", "doc", "answer_snippet"]
    target_id: str
    vote: Literal[-1, 0, 1]
    created_at: datetime | None = None


class Query(BaseModel):
    id: int | None = None
    user_id: int
    query_text: str
    created_at: datetime | None = None


class Preference(BaseModel):
    id: int | None = None
    user_id: int
    tag: str
    weight: float = 0.0
    updated_at: datetime | None = None


class Trend(BaseModel):
    id: int | None = None
    user_id: int
    metric: str
    time_window: Literal["15m", "1h", "24h"]
    tag: str
    value: float
    computed_at: datetime | None = None
