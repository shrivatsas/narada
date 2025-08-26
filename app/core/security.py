from collections.abc import Mapping
from datetime import UTC, datetime, timedelta
from typing import Any, cast

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(p: str) -> str:
    # passlib returns a str-like value; coerce to str for typing
    return str(pwd_ctx.hash(p))


def verify_password(p: str, hp: str) -> bool:
    return bool(pwd_ctx.verify(p, hp))


def make_token(user_id: int, expires_minutes: int = 60 * 24 * 7) -> str:
    now = datetime.now(UTC)
    payload = {
        "sub": str(user_id),
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=expires_minutes)).timestamp()),
    }
    token: str = cast(str, jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_alg))
    return token


def parse_token(token: str) -> int:
    decoded: Mapping[str, Any] = cast(
        Mapping[str, Any],
        jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_alg]),
    )
    return int(decoded["sub"])  # user_id
