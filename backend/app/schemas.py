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
    fall_budget_per_user: float
    spring_budget_per_user: float
    status: SeasonStatus

    model_config = {"from_attributes": True}


class SeasonCreateIn(BaseModel):
    name: str
    # $440, not $400 -- covers the 4 extra UCL roster slots added mid-cycle
    # to the fall session (see app/set_ev_defaults.py's matching default).
    fall_budget_per_user: float = 440
    spring_budget_per_user: float = 240


class TeamOut(BaseModel):
    id: int
    league: str
    sport: str
    name: str
    default_value: float | None = None

    model_config = {"from_attributes": True}


class TeamHistorySeasonOut(BaseModel):
    season_label: str
    points: float


class TeamHistoryOut(BaseModel):
    team_id: int
    league: str
    name: str
    bio: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    prognosis: str | None = None
    seasons: list[TeamHistorySeasonOut] = []


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


class ReserveBidOut(BaseModel):
    amount: float
    active: bool


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
    # Private to the viewer — only ever populated with the requesting
    # user's own reserve, never anyone else's (see build_state). None if
    # they don't have one set on this item.
    my_reserve: ReserveBidOut | None = None

    model_config = {"from_attributes": True}


class NominateIn(BaseModel):
    team_id: int


class ForceTurnIn(BaseModel):
    user_id: int


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
    # True during the nightly 9 PM-9 AM Eastern quiet-hours window --
    # server-computed so the frontend doesn't need its own timezone/DST
    # logic. Purely informational: nomination/bid deadlines already skip
    # this window on their own (see app/quiet_hours.py), so this only
    # drives display (e.g. showing "quiet hours" instead of a ticking
    # countdown) — it doesn't gate bidding, passing, or reserves at all.
    is_quiet_hours: bool
    # When it's someone's turn to nominate, the actual wall-clock deadline
    # schedule_turn_timer will auto-nominate at — already adjusted to skip
    # quiet hours, so the frontend can count down to this directly instead
    # of re-deriving (and getting wrong) auction.turn_started_at +
    # NOMINATION_TIMEOUT_SECONDS itself. None when an item is active (no
    # turn is open) or the auction has no nomination order yet.
    nomination_deadline: datetime | None


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
    breakdown: list[ScoringRuleLine]


class QueueEntryOut(BaseModel):
    id: int
    user_id: int
    team: TeamOut
    order: int
    reserve_price: float | None
    nomination_price: float | None

    model_config = {"from_attributes": True}


class QueueAddIn(BaseModel):
    team_id: int


class QueueMoveIn(BaseModel):
    direction: Literal["up", "down"]


class QueueReservePriceIn(BaseModel):
    # None clears the reserve — the team stays queued, it just won't get an
    # automatic reserve bid applied once it comes up for auction.
    reserve_price: float | None


class QueueNominationPriceIn(BaseModel):
    # None falls back to the app's standard $1 opening bid.
    nomination_price: float | None


class CribSheetEntryOut(BaseModel):
    id: int
    team_id: int
    value: float

    model_config = {"from_attributes": True}


class CribSheetSetIn(BaseModel):
    value: float
