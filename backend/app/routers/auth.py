import jwt
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.auth import create_magic_link_token, create_session_token, verify_magic_link_token
from app.config import settings
from app.database import get_db
from app.deps import SESSION_COOKIE_NAME, get_current_user
from app.email import send_magic_link
from app.models import User
from app.schemas import RequestLinkIn, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/request-link", status_code=status.HTTP_202_ACCEPTED)
def request_link(payload: RequestLinkIn, db: Session = Depends(get_db)):
    email = payload.email.lower()

    # Always respond 202 regardless of allow-list membership, so we don't leak
    # who is/isn't a league member to an unauthenticated caller.
    user = db.query(User).filter(User.email == email).first()
    if user is not None:
        token = create_magic_link_token(email)
        link = f"{settings.api_base_url}/api/auth/verify?token={token}"
        send_magic_link(email, link)

    return {"message": "If that email is registered, a login link has been sent."}


@router.get("/verify")
def verify(token: str, db: Session = Depends(get_db)):
    try:
        email = verify_magic_link_token(token)
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired link")

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unknown user")

    session_token = create_session_token(user.id)
    redirect = RedirectResponse(url=f"{settings.app_base_url}/")
    redirect.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=session_token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
        max_age=settings.session_ttl_days * 24 * 60 * 60,
    )
    return redirect


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(SESSION_COOKIE_NAME)
    return {"message": "logged out"}


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user
