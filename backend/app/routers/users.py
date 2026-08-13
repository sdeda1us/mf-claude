from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import User
from app.schemas import UserOut, UserUpdateIn

router = APIRouter(prefix="/users", tags=["users"])

# Data URL string length cap (base64 has ~33% overhead, so this allows
# roughly a 500KB image) — generous for a small resized avatar, small enough
# to keep the row (and every API response that embeds it) reasonable.
MAX_AVATAR_DATA_URL_LENGTH = 700_000


@router.get("", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(User).order_by(User.display_name).all()


@router.put("/me", response_model=UserOut)
def update_me(
    payload: UserUpdateIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    display_name = payload.display_name.strip()
    if not display_name:
        raise HTTPException(status_code=400, detail="Display name can't be empty")
    if len(display_name) > 100:
        raise HTTPException(status_code=400, detail="Display name is too long")

    # None means "leave the avatar as-is"; "" explicitly clears it; anything
    # else must be an image data URL.
    if payload.avatar_data_url == "":
        user.avatar_data_url = None
    elif payload.avatar_data_url is not None:
        if not payload.avatar_data_url.startswith("data:image/"):
            raise HTTPException(status_code=400, detail="Avatar must be an image")
        if len(payload.avatar_data_url) > MAX_AVATAR_DATA_URL_LENGTH:
            raise HTTPException(status_code=400, detail="Avatar image is too large")
        user.avatar_data_url = payload.avatar_data_url

    user.display_name = display_name
    db.commit()
    db.refresh(user)
    return user
