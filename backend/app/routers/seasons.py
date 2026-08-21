from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_commissioner, get_current_user
from app.models import Season, User
from app.schemas import SeasonCreateIn, SeasonOut

router = APIRouter(prefix="/seasons", tags=["seasons"])


@router.get("", response_model=list[SeasonOut])
def list_seasons(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Season).order_by(Season.created_at.desc()).all()


@router.post("", response_model=SeasonOut, status_code=201)
def create_season(
    payload: SeasonCreateIn,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_commissioner),
):
    season = Season(
        name=payload.name,
        fall_budget_per_user=payload.fall_budget_per_user,
        spring_budget_per_user=payload.spring_budget_per_user,
    )
    db.add(season)
    db.commit()
    db.refresh(season)
    return season
