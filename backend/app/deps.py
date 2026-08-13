import jwt
from fastapi import Cookie, Depends, HTTPException, WebSocket, status
from sqlalchemy.orm import Session

from app.auth import verify_session_token
from app.database import get_db
from app.models import User

SESSION_COOKIE_NAME = "megafantasy_session"


def _load_user(db: Session, token: str | None) -> User:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        user_id = verify_session_token(token)
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session")
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unknown user")
    return user


def get_current_user(
    db: Session = Depends(get_db),
    session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE_NAME),
) -> User:
    return _load_user(db, session_token)


def get_current_commissioner(user: User = Depends(get_current_user)) -> User:
    if not user.is_commissioner:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Commissioner only")
    return user


def get_user_from_websocket(websocket: WebSocket, db: Session) -> User:
    token = websocket.cookies.get(SESSION_COOKIE_NAME)
    return _load_user(db, token)
