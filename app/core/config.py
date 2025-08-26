import os

from pydantic import BaseModel


class Settings(BaseModel):
    database_url: str = os.getenv(
        "DATABASE_URL", "postgresql+psycopg://app:app@localhost:5432/discovery"
    )
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    jwt_secret: str = os.getenv("JWT_SECRET", "change-me")
    jwt_alg: str = os.getenv("JWT_ALG", "HS256")
    embed_model: str = os.getenv("EMBED_MODEL", "intfloat/e5-small-v2")
    daily_digest_hour_ist: int = int(os.getenv("DAILY_DIGEST_HOUR_IST", "9"))


settings = Settings()
