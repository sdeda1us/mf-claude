from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import CribSheetEntry, Team, User
from app.schemas import CribSheetEntryOut, CribSheetSetIn

router = APIRouter(prefix="/crib-sheet", tags=["crib-sheet"])


@router.get("", response_model=list[CribSheetEntryOut])
def list_crib_sheet(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(CribSheetEntry).filter(CribSheetEntry.user_id == user.id).all()


@router.put("/{team_id}", response_model=CribSheetEntryOut)
def set_crib_sheet_value(
    team_id: int,
    payload: CribSheetSetIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if db.get(Team, team_id) is None:
        raise HTTPException(status_code=404, detail="Team not found")

    entry = (
        db.query(CribSheetEntry)
        .filter(CribSheetEntry.user_id == user.id, CribSheetEntry.team_id == team_id)
        .first()
    )
    if entry is None:
        entry = CribSheetEntry(user_id=user.id, team_id=team_id, value=payload.value)
        db.add(entry)
    else:
        entry.value = payload.value
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/{team_id}", status_code=204)
def clear_crib_sheet_value(
    team_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    entry = (
        db.query(CribSheetEntry)
        .filter(CribSheetEntry.user_id == user.id, CribSheetEntry.team_id == team_id)
        .first()
    )
    if entry is not None:
        db.delete(entry)
        db.commit()
