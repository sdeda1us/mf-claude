from datetime import datetime, timedelta, timezone

import jwt

from app.config import settings

MAGIC_LINK_SCOPE = "magic_link"
SESSION_SCOPE = "session"


def create_magic_link_token(email: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": email.lower(),
        "scope": MAGIC_LINK_SCOPE,
        "iat": now,
        "exp": now + timedelta(minutes=settings.magic_link_ttl_minutes),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def verify_magic_link_token(token: str) -> str:
    """Returns the email if valid, raises jwt exceptions otherwise."""
    payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    if payload.get("scope") != MAGIC_LINK_SCOPE:
        raise jwt.InvalidTokenError("wrong token scope")
    return payload["sub"]


def create_session_token(user_id: int) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "scope": SESSION_SCOPE,
        "iat": now,
        "exp": now + timedelta(days=settings.session_ttl_days),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def verify_session_token(token: str) -> int:
    """Returns the user id if valid, raises jwt exceptions otherwise."""
    payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    if payload.get("scope") != SESSION_SCOPE:
        raise jwt.InvalidTokenError("wrong token scope")
    return int(payload["sub"])
