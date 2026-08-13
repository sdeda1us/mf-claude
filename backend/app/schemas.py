from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr

from app.models import AuctionItemStatus, AuctionStatus, RosterSource, SeasonStatus


class RequestLinkIn(BaseModel):
    email: EmailStr


class UserOut(BaseModel):
    id: int
    email: str
    display_name: str
    is_commissioner: bool
    avatar_data_url: str | None

    model_config = {"from_attributes": True}


class UserUpdateIn(BaseModel):
    display_name: str
    avatar_data_url: str | None = None


class SeasonOut(BaseModel):
    id: int
    name: str
    budget_per_user: float
    status: SeasonStatus

    model_config = {"from_attributes": True}


class SeasonCreateIn(BaseModel):
    name: str
    budget_per_user: float = 600


class TeamOut(BaseModel):
    id: int
    league: str
    sport: str
    name: str

    model_config = {"from_attributes": True}


class AuctionOut(BaseModel):
    id: int
    season_id: int
    session: str
    status: AuctionStatus
    nomination_order: list[int]
    turn_started_at: datetime
    is_paused: bool

    model_config = {"from_attributes": True}


class BidOut(BaseModel):
    id: int
    user_id: int
    amount: float
    created_at: datetime

    model_config = {"from_attributes": True}


class AuctionItemOut(BaseModel):
    id: int
    auction_id: int
    team: TeamOut
    order: int
    status: AuctionItemStatus
    winning_user_id: int | None
    winning_bid: float | None
    bids: list[BidOut] = []
    bid_deadline: datetime | None
    passed_user_ids: list[int] = []

    model_config = {"from_attributes": True}


class NominateIn(BaseModel):
    team_id: int


class RosterEntryOut(BaseModel):
    id: int
    user_id: int
    team: TeamOut
    price_paid: float
    source: RosterSource

    model_config = {"from_attributes": True}


class RosterCorrectionIn(BaseModel):
    user_id: int
    team_id: int
    price_paid: float


class RosterStatusOut(BaseModel):
    budget_remaining: float
    spots_filled: int
    spots_remaining: int
    max_bid: float


class AuctionStateOut(BaseModel):
    auction: AuctionOut
    active_item: AuctionItemOut | None
    remaining_budget_by_user: dict[int, float]
    current_turn_user_id: int | None
    roster_status_by_user: dict[int, RosterStatusOut]


class ScoringRuleLine(BaseModel):
    label: str
    points: float


class LeagueRulesOut(BaseModel):
    roster_limits: dict[str, int]
    scoring_rules: dict[str, list[ScoringRuleLine]]
    league_session: dict[str, str]
    # League -> minor-conference team names in that league (currently only
    # populated for NCAAF/NCAAMB/NCAAWB) — hidden by default on the crib
    # sheet given how many of them there are, searchable to add back.
    minor_conference_teams: dict[str, list[str]]


class ExampleScoreOut(BaseModel):
    team_id: int
    team_name: str
    league: str
    season_label: str
    points: float


class QueueEntryOut(BaseModel):
    id: int
    user_id: int
    team: TeamOut
    order: int

    model_config = {"from_attributes": True}


class QueueAddIn(BaseModel):
    team_id: int


class QueueMoveIn(BaseModel):
    direction: Literal["up", "down"]


class CribSheetEntryOut(BaseModel):
    id: int
    team_id: int
    value: float

    model_config = {"from_attributes": True}


class CribSheetSetIn(BaseModel):
    value: float
