from collections import defaultdict
from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.daily_results_sync import RESULT_MATCH_LOOKBACK_DAYS
from app.daily_score_sync import today_eastern
from app.database import get_db
from app.deps import get_current_commissioner, get_current_user
from app.league_rules import compute_score
from app.models import (
    Auction,
    AuctionItem,
    Bid,
    QueueEntry,
    ReserveBid,
    RosterEntry,
    ScheduledGame,
    Season,
    SeasonStatus,
    Team,
    TeamDailyScore,
    TeamSeasonResult,
    User,
)
from app.schemas import (
    LeagueEventOut,
    LeagueTeamScoreOut,
    LeagueWeeklyGainOut,
    OwnerScoreHistoryOut,
    ScoreHistoryOut,
    ScoreHistoryPointOut,
    ScoringSummaryOut,
    ScoringSummaryOwnerOut,
    SeasonCreateIn,
    SeasonOut,
    TodaysGameOut,
    YesterdaysResultOut,
    YesterdaysScoringByPlayerOut,
    YesterdaysScoringByPlayerOwnerOut,
)
from app.scoring_events import diff_team_events
from app.season_labels import CURRENT_SEASON, ZERO_STATS

router = APIRouter(prefix="/seasons", tags=["seasons"])

# Every league in the fall auction session (see LEAGUE_SESSION) except
# NCAAMB/NCAAWB, which are deliberately left out -- their pools are ~360
# teams each and their 2026-27 season hasn't even started yet, so there's
# no way to source that scale of data reliably. Unlike EPL/URC (every
# team in those two IS drafted, so their column is a full standings
# preview), most of these leagues still have plenty of undrafted teams
# sitting in the auction pool -- update_live_standings.py only seeds
# whichever teams actually appear on a roster right now, by design, so a
# league's column here only ever reflects the teams someone's actually
# drafted, not the whole league.
SCORING_SUMMARY_LEAGUES = ["NFL", "NBA", "NHL", "EPL", "UCL", "URC", "NCAAF", "ATP", "WTA"]

# Same 7 leagues as SCORING_SUMMARY_LEAGUES minus ATP/WTA -- those two are
# country/individual-match aggregates with no single "team vs team" game
# to show in a schedule widget.
TODAYS_GAMES_LEAGUES = [lg for lg in SCORING_SUMMARY_LEAGUES if lg not in ("ATP", "WTA")]


@router.get("", response_model=list[SeasonOut])
def list_seasons(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Season).order_by(Season.created_at.desc()).all()


@router.get("/{season_id}/scoring-summary", response_model=ScoringSummaryOut)
def scoring_summary(
    season_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    """Per-owner points for the leagues in SCORING_SUMMARY_LEAGUES, from
    each drafted team's most recent TeamSeasonResult (whichever
    season_label sorts latest, per team -- see results_by_team below) --
    the current, in-progress 2026-27 season for every league here, kept
    current by re-running app/update_live_standings.py against a fresh
    table lookup (there's no live sports-data feed wired into this app,
    so nothing updates these rows on its own). A team with no
    TeamSeasonResult row at all (undrafted, or drafted but not yet
    scored) silently contributes 0 rather than erroring, same spirit as
    /leagues/example-scores -- this is deliberate for most of these
    leagues, where update_live_standings.py only ever seeds rows for
    teams someone's actually drafted, not the whole league."""
    if db.get(Season, season_id) is None:
        raise HTTPException(status_code=404, detail="Season not found")

    entries = (
        db.query(RosterEntry)
        .join(Team, RosterEntry.team_id == Team.id)
        .filter(RosterEntry.season_id == season_id, Team.league.in_(SCORING_SUMMARY_LEAGUES))
        .all()
    )
    # Ordered oldest-label-first so that when a team has more than one
    # season's row (e.g. "2025-26" and "2026-27"), the later one wins this
    # dict's last-write-wins overwrite -- season labels sort chronologically
    # as plain strings ("2026-27" > "2025-26"), so no separate date field
    # is needed to know which is newer.
    results_by_team = {
        r.team_id: r
        for r in db.query(TeamSeasonResult)
        .filter(TeamSeasonResult.league.in_(SCORING_SUMMARY_LEAGUES))
        .order_by(TeamSeasonResult.season_label.asc())
    }
    # A team has "started playing and counting towards scoring" once the
    # daily sync has written at least one TeamDailyScore row for its
    # current real-world season -- same proxy league_weekly_gains/
    # league_events use to skip never-synced teams, rather than a
    # dedicated started/not-started flag (there isn't one in the schema).
    team_ids = {e.team_id for e in entries}
    started_team_ids = {
        row.team_id
        for row in db.query(
            TeamDailyScore.team_id, TeamDailyScore.league, TeamDailyScore.season_label
        )
        .filter(
            TeamDailyScore.team_id.in_(team_ids),
            TeamDailyScore.league.in_(SCORING_SUMMARY_LEAGUES),
        )
        .all()
        if row.season_label == CURRENT_SEASON.get(row.league)
    }

    season_label_by_league: dict[str, str] = {}
    totals: dict[int, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    dollars_counted: dict[int, float] = defaultdict(float)
    for entry in entries:
        result = results_by_team.get(entry.team_id)
        if result is None:
            continue
        league = entry.team.league
        season_label_by_league.setdefault(league, result.season_label)
        totals[entry.user_id][league] += compute_score(league, result.stats)
        if entry.team_id in started_team_ids:
            dollars_counted[entry.user_id] += float(entry.price_paid)

    owners = [
        ScoringSummaryOwnerOut(
            user_id=u.id,
            display_name=u.display_name,
            by_league={lg: totals[u.id].get(lg, 0.0) for lg in SCORING_SUMMARY_LEAGUES},
            total=sum(totals[u.id].values()),
            ppd=(sum(totals[u.id].values()) / dollars_counted[u.id]) if dollars_counted.get(u.id) else 0.0,
        )
        for u in db.query(User).all()
    ]
    owners.sort(key=lambda o: o.total, reverse=True)

    return ScoringSummaryOut(
        leagues=SCORING_SUMMARY_LEAGUES,
        season_label_by_league=season_label_by_league,
        owners=owners,
    )


@router.get("/{season_id}/score-history", response_model=ScoreHistoryOut)
def score_history(
    season_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    """Each owner's cumulative SCORING_SUMMARY_LEAGUES total for every
    real-world day any of their rostered teams has TeamDailyScore history
    -- the Home page's score-over-time chart, sitting right below the Fall
    Scoring Summary table. A team contributes 0 for days before its first
    tracked row and is forward-filled at its last known score between
    rows (most days won't have a fresh sync for every team), same
    precedent as _team_point_change's day-to-day diffing. daily_change is
    what that day added to the owner's running total -- for a team's
    first-ever tracked day (backdated, see TeamDailyScore's docstring)
    that's the same as its cumulative score, since there's nothing earlier
    to diff against."""
    if db.get(Season, season_id) is None:
        raise HTTPException(status_code=404, detail="Season not found")

    entries = (
        db.query(RosterEntry)
        .join(Team, RosterEntry.team_id == Team.id)
        .filter(RosterEntry.season_id == season_id, Team.league.in_(SCORING_SUMMARY_LEAGUES))
        .all()
    )
    user_by_team: dict[int, int] = {e.team_id: e.user_id for e in entries}
    if not user_by_team:
        return ScoreHistoryOut(owners=[])

    rows = (
        db.query(TeamDailyScore)
        .filter(
            TeamDailyScore.team_id.in_(user_by_team.keys()),
            TeamDailyScore.league.in_(SCORING_SUMMARY_LEAGUES),
        )
        .order_by(TeamDailyScore.as_of_date.asc())
        .all()
    )
    # Only this team's CURRENT real-world season -- same guard as
    # scoring_summary's started_team_ids, so a stale prior season's rows
    # (if any ever existed) can't leak into this chart.
    rows = [r for r in rows if r.season_label == CURRENT_SEASON.get(r.league)]
    if not rows:
        return ScoreHistoryOut(owners=[])

    rows_by_team: dict[int, list[TeamDailyScore]] = defaultdict(list)
    for r in rows:
        rows_by_team[r.team_id].append(r)

    all_dates = sorted({r.as_of_date for r in rows})

    cumulative_by_user: dict[int, dict[date, float]] = defaultdict(lambda: defaultdict(float))
    for team_id, team_rows in rows_by_team.items():
        owner_id = user_by_team.get(team_id)
        if owner_id is None:
            continue
        by_date = {r.as_of_date: float(r.score) for r in team_rows}
        first_date = team_rows[0].as_of_date
        last_known = 0.0
        for d in all_dates:
            if d < first_date:
                continue
            if d in by_date:
                last_known = by_date[d]
            cumulative_by_user[owner_id][d] += last_known

    users_by_id = {u.id: u for u in db.query(User).all()}
    owners = []
    for user_id, by_date in cumulative_by_user.items():
        user = users_by_id.get(user_id)
        if user is None:
            continue
        prev = 0.0
        points = []
        for d in all_dates:
            cum = by_date.get(d, 0.0)
            points.append(ScoreHistoryPointOut(date=d.isoformat(), cumulative=cum, daily_change=cum - prev))
            prev = cum
        owners.append(OwnerScoreHistoryOut(user_id=user_id, display_name=user.display_name, points=points))

    owners.sort(key=lambda o: o.points[-1].cumulative if o.points else 0.0, reverse=True)

    return ScoreHistoryOut(owners=owners)


@router.get("/{season_id}/todays-games", response_model=list[TodaysGameOut])
def todays_games(
    season_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    """Today's real-world schedule across TODAYS_GAMES_LEAGUES, with the
    owning player (if any, for this season) attached to each side -- the
    Home page's "Today's Games" widget. A game where NEITHER side is
    rostered this season is dropped entirely (nobody's fantasy score
    depends on it); a game where at least one side is rostered still
    shows, with owner=None on whichever side is undrafted or unmatched
    (daily_games_sync.sync_games_for_date couldn't resolve that team's
    name to a Team row)."""
    if db.get(Season, season_id) is None:
        raise HTTPException(status_code=404, detail="Season not found")

    games = (
        db.query(ScheduledGame)
        .filter(
            ScheduledGame.game_date == today_eastern(),
            ScheduledGame.league.in_(TODAYS_GAMES_LEAGUES),
        )
        .all()
    )

    team_ids = {g.home_team_id for g in games if g.home_team_id} | {
        g.away_team_id for g in games if g.away_team_id
    }
    owner_by_team_id: dict[int, str] = {}
    if team_ids:
        users_by_id = {u.id: u for u in db.query(User).all()}
        for e in (
            db.query(RosterEntry)
            .filter(RosterEntry.season_id == season_id, RosterEntry.team_id.in_(team_ids))
            .all()
        ):
            owner_by_team_id[e.team_id] = (
                users_by_id[e.user_id].display_name
                if e.user_id in users_by_id
                else f"User #{e.user_id}"
            )

    # Drop games where neither side is drafted -- a fantasy player only
    # cares about a game if it's scoring points for someone's roster.
    games = [g for g in games if g.home_team_id in owner_by_team_id or g.away_team_id in owner_by_team_id]

    league_order = {lg: i for i, lg in enumerate(TODAYS_GAMES_LEAGUES)}
    games.sort(key=lambda g: (league_order.get(g.league, len(TODAYS_GAMES_LEAGUES)), g.home_team_name))

    return [
        TodaysGameOut(
            league=g.league,
            home_team_id=g.home_team_id,
            home_team_name=g.home_team_name,
            home_owner=owner_by_team_id.get(g.home_team_id) if g.home_team_id else None,
            away_team_id=g.away_team_id,
            away_team_name=g.away_team_name,
            away_owner=owner_by_team_id.get(g.away_team_id) if g.away_team_id else None,
            venue=g.venue,
            time_label=g.time_label,
        )
        for g in games
    ]


def _team_point_change(db: Session, team_id: int, league: str, as_of_date) -> float | None:
    """This team's TeamDailyScore delta for as_of_date vs. its most recent
    earlier row -- i.e. what that result added to (or cost) its owner's
    total. None if as_of_date has no row yet, or has no earlier row to
    diff against (the team's first-ever tracked day, which is backdated
    and not a real delta -- see daily_score_sync's module docstring).

    Callers attributing a GAME played on day D must pass today_eastern()
    here, not D itself: every sync (daily_score_sync, nhl_standings_sync)
    stamps its row with the date it RAN, which is always the morning
    after the games it reflects -- a game played the night of day D shows
    up in the row dated D+1, since the row for D itself was already
    written that morning, before D's games happened. Passing D would
    silently diff two rows that both predate the game and always return
    0.0 instead of the real change (see yesterdays_results below)."""
    season_label = CURRENT_SEASON.get(league)
    if season_label is None:
        return None
    rows = (
        db.query(TeamDailyScore)
        .filter(
            TeamDailyScore.team_id == team_id,
            TeamDailyScore.season_label == season_label,
            TeamDailyScore.as_of_date <= as_of_date,
        )
        .order_by(TeamDailyScore.as_of_date.desc())
        .limit(2)
        .all()
    )
    if len(rows) < 2 or rows[0].as_of_date != as_of_date:
        return None
    return float(rows[0].score - rows[1].score)


@router.get("/{season_id}/yesterdays-results", response_model=list[YesterdaysResultOut])
def yesterdays_results(
    season_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    """Yesterday's concluded games across TODAYS_GAMES_LEAGUES, with final
    score, owning player (if any), and each owned side's fantasy-point
    change for the day -- the Home page's "Yesterday's Results" card,
    sitting next to "Today's Games". Same "drop it if nobody owns either
    side" rule as todays_games.

    Also includes any STILL-UNRESOLVED game (home_score/away_score null)
    from the last RESULT_MATCH_LOOKBACK_DAYS, not just exactly yesterday's
    -- with those fields None in the response, i.e. "pending" rather than
    a final score. Without this, a game whose games-sync guessed the
    wrong date (a rescheduled kickoff, a postponement) would otherwise
    vanish the moment "yesterday" moves past its date, with nothing in
    the UI to show it was ever scheduled or that it's still awaiting a
    result. Once daily_results_sync's own lookback fallback (see
    RESULT_MATCH_LOOKBACK_DAYS there) finally attaches that game's real
    result, it corrects the row's game_date to match -- which is always
    "yesterday" from the pull that processes it -- so a since-resolved
    game surfaces through the normal exactly-yesterday branch below
    rather than needing special handling here too."""
    if db.get(Season, season_id) is None:
        raise HTTPException(status_code=404, detail="Season not found")

    today = today_eastern()
    yesterday = today - timedelta(days=1)
    games = (
        db.query(ScheduledGame)
        .filter(
            ScheduledGame.league.in_(TODAYS_GAMES_LEAGUES),
            ScheduledGame.game_date <= yesterday,
            ScheduledGame.game_date > yesterday - timedelta(days=RESULT_MATCH_LOOKBACK_DAYS),
            or_(
                and_(
                    ScheduledGame.game_date == yesterday,
                    ScheduledGame.home_score.is_not(None),
                    ScheduledGame.away_score.is_not(None),
                ),
                ScheduledGame.home_score.is_(None),
            ),
        )
        .all()
    )

    team_ids = {g.home_team_id for g in games if g.home_team_id} | {
        g.away_team_id for g in games if g.away_team_id
    }
    owner_by_team_id: dict[int, str] = {}
    if team_ids:
        users_by_id = {u.id: u for u in db.query(User).all()}
        for e in (
            db.query(RosterEntry)
            .filter(RosterEntry.season_id == season_id, RosterEntry.team_id.in_(team_ids))
            .all()
        ):
            owner_by_team_id[e.team_id] = (
                users_by_id[e.user_id].display_name
                if e.user_id in users_by_id
                else f"User #{e.user_id}"
            )

    # Same "drop it if nobody owns either side" rule as todays_games.
    games = [g for g in games if g.home_team_id in owner_by_team_id or g.away_team_id in owner_by_team_id]

    league_order = {lg: i for i, lg in enumerate(TODAYS_GAMES_LEAGUES)}
    games.sort(key=lambda g: (league_order.get(g.league, len(TODAYS_GAMES_LEAGUES)), g.home_team_name))

    return [
        YesterdaysResultOut(
            league=g.league,
            home_team_id=g.home_team_id,
            home_team_name=g.home_team_name,
            home_owner=owner_by_team_id.get(g.home_team_id) if g.home_team_id else None,
            home_score=g.home_score,
            home_point_change=(
                _team_point_change(db, g.home_team_id, g.league, today)
                if g.home_team_id in owner_by_team_id
                else None
            ),
            away_team_id=g.away_team_id,
            away_team_name=g.away_team_name,
            away_owner=owner_by_team_id.get(g.away_team_id) if g.away_team_id else None,
            away_score=g.away_score,
            away_point_change=(
                _team_point_change(db, g.away_team_id, g.league, today)
                if g.away_team_id in owner_by_team_id
                else None
            ),
        )
        for g in games
    ]


@router.get(
    "/{season_id}/yesterdays-scoring-by-player", response_model=YesterdaysScoringByPlayerOut
)
def yesterdays_scoring_by_player(
    season_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    """Each owner's point change since the last daily sync, by league --
    the table at the top of the Home page's Yesterday's Results column.

    Deliberately NOT built from yesterdays_results' game list: that one
    only attributes a point change to a team if it has a ScheduledGame row
    dated exactly yesterday (or still pending), so a team whose matching
    game is missing entirely (an ESPN games-sync miss) or dated further
    back (a standings sync catching up several days at once) silently
    drops out of it -- while its TeamDailyScore history (and so the Score
    Over Time chart below, which has no such gating) still reflects the
    real change. Using _team_point_change directly against every rostered
    team here, the same way score_history does for its own latest day,
    keeps this table's totals equal to the chart's daily_change for
    today, closing that gap. TODAYS_GAMES_LEAGUES only (not the full
    SCORING_SUMMARY_LEAGUES) -- ATP/WTA have no day-to-day sync to diff,
    same reasoning as yesterdays_results/todays_games excluding them."""
    if db.get(Season, season_id) is None:
        raise HTTPException(status_code=404, detail="Season not found")

    today = today_eastern()
    entries = (
        db.query(RosterEntry)
        .join(Team, RosterEntry.team_id == Team.id)
        .filter(RosterEntry.season_id == season_id, Team.league.in_(TODAYS_GAMES_LEAGUES))
        .all()
    )

    totals: dict[int, dict[str, float]] = {}
    for e in entries:
        change = _team_point_change(db, e.team_id, e.team.league, today)
        if change is None:
            continue
        user_totals = totals.setdefault(e.user_id, {})
        user_totals[e.team.league] = user_totals.get(e.team.league, 0.0) + change

    owners = [
        YesterdaysScoringByPlayerOwnerOut(
            user_id=u.id,
            display_name=u.display_name,
            by_league=totals[u.id],
            total=sum(totals[u.id].values()),
        )
        for u in db.query(User).all()
        if u.id in totals
    ]
    owners.sort(key=lambda o: o.total, reverse=True)

    return YesterdaysScoringByPlayerOut(leagues=TODAYS_GAMES_LEAGUES, owners=owners)


@router.get("/{season_id}/leagues/{league}/team-scores", response_model=list[LeagueTeamScoreOut])
def league_team_scores(
    season_id: int, league: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    """Per-team points within a single league -- the breakdown behind one
    cell of scoring_summary's by_league total, used by the Seasons page's
    stacked-bar chart (one segment per team a player owns in that
    league)."""
    if db.get(Season, season_id) is None:
        raise HTTPException(status_code=404, detail="Season not found")

    entries = (
        db.query(RosterEntry)
        .join(Team, RosterEntry.team_id == Team.id)
        .filter(RosterEntry.season_id == season_id, Team.league == league)
        .all()
    )
    # Same "most recent by season_label" resolution as scoring_summary.
    results_by_team = {
        r.team_id: r
        for r in db.query(TeamSeasonResult)
        .filter(TeamSeasonResult.league == league)
        .order_by(TeamSeasonResult.season_label.asc())
    }
    users_by_id = {u.id: u for u in db.query(User).all()}

    return [
        LeagueTeamScoreOut(
            user_id=e.user_id,
            display_name=users_by_id[e.user_id].display_name
            if e.user_id in users_by_id
            else f"User #{e.user_id}",
            team_id=e.team_id,
            team_name=e.team.name,
            price_paid=e.price_paid,
            points=compute_score(league, results_by_team[e.team_id].stats)
            if e.team_id in results_by_team
            else 0.0,
        )
        for e in entries
    ]


@router.get("/{season_id}/leagues/{league}/weekly-gains", response_model=list[LeagueWeeklyGainOut])
def league_weekly_gains(
    season_id: int, league: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    """How much each rostered team's score has moved over its last 7 days
    of TeamDailyScore history -- the "who's hot this week" chart below the
    Seasons page's standings chart. Sorted highest gain first; a team with
    no daily-score history yet (never synced) is left out rather than
    shown with a meaningless 0. days_tracked can be less than 7 for a team
    whose history doesn't go back that far yet."""
    if db.get(Season, season_id) is None:
        raise HTTPException(status_code=404, detail="Season not found")

    season_label = CURRENT_SEASON.get(league)
    if season_label is None:
        return []

    entries = (
        db.query(RosterEntry)
        .join(Team, RosterEntry.team_id == Team.id)
        .filter(RosterEntry.season_id == season_id, Team.league == league)
        .all()
    )
    users_by_id = {u.id: u for u in db.query(User).all()}

    results: list[LeagueWeeklyGainOut] = []
    for e in entries:
        daily_rows = (
            db.query(TeamDailyScore)
            .filter(TeamDailyScore.team_id == e.team_id, TeamDailyScore.season_label == season_label)
            .order_by(TeamDailyScore.as_of_date.asc())
            .all()
        )
        if not daily_rows:
            continue
        latest = daily_rows[-1]
        cutoff = latest.as_of_date - timedelta(days=6)
        window = [r for r in daily_rows if r.as_of_date >= cutoff]
        baseline = window[0]
        results.append(
            LeagueWeeklyGainOut(
                team_id=e.team_id,
                team_name=e.team.name,
                user_id=e.user_id,
                display_name=users_by_id[e.user_id].display_name
                if e.user_id in users_by_id
                else f"User #{e.user_id}",
                gain=float(latest.score) - float(baseline.score),
                latest_score=float(latest.score),
                days_tracked=(latest.as_of_date - baseline.as_of_date).days + 1,
            )
        )

    results.sort(key=lambda r: r.gain, reverse=True)
    return results


@router.get("/{season_id}/leagues/{league}/events", response_model=list[LeagueEventOut])
def league_events(
    season_id: int, league: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    """What each rostered team picked up (or lost) points for, and on
    which day -- the Seasons page's "Recent Activity" feed. Diffs each
    team's consecutive TeamDailyScore rows (see scoring_events.
    diff_team_events); a team's first-ever row is diffed against an
    all-zero baseline so day one's cumulative state shows up too. Limited
    to the last 7 days, newest first -- same window as weekly-gains
    above."""
    if db.get(Season, season_id) is None:
        raise HTTPException(status_code=404, detail="Season not found")

    season_label = CURRENT_SEASON.get(league)
    if season_label is None:
        return []

    entries = (
        db.query(RosterEntry)
        .join(Team, RosterEntry.team_id == Team.id)
        .filter(RosterEntry.season_id == season_id, Team.league == league)
        .all()
    )
    users_by_id = {u.id: u for u in db.query(User).all()}
    cutoff = today_eastern() - timedelta(days=6)

    results: list[LeagueEventOut] = []
    for e in entries:
        daily_rows = (
            db.query(TeamDailyScore)
            .filter(TeamDailyScore.team_id == e.team_id, TeamDailyScore.season_label == season_label)
            .order_by(TeamDailyScore.as_of_date.asc())
            .all()
        )
        if not daily_rows:
            continue
        display_name = (
            users_by_id[e.user_id].display_name if e.user_id in users_by_id else f"User #{e.user_id}"
        )
        prev_stats = ZERO_STATS.get(league, {})
        for row in daily_rows:
            if row.as_of_date >= cutoff:
                for event in diff_team_events(league, prev_stats, row.stats):
                    results.append(
                        LeagueEventOut(
                            as_of_date=row.as_of_date.isoformat(),
                            team_id=e.team_id,
                            team_name=e.team.name,
                            user_id=e.user_id,
                            display_name=display_name,
                            label=event["label"],
                            points=event["points"],
                        )
                    )
            prev_stats = row.stats

    results.sort(key=lambda r: r.as_of_date, reverse=True)
    return results


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


@router.post("/{season_id}/activate", response_model=SeasonOut)
def activate_season(
    season_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_commissioner),
):
    """Marks this the active season (the one Home.tsx shows snapshots for)
    and demotes whichever season previously held that status to "complete"
    -- only one season is ever *the* active one, and a newly-activated
    season superseding another reads truer as that other one being done
    than as it reverting to "setup"."""
    season = db.get(Season, season_id)
    if season is None:
        raise HTTPException(status_code=404, detail="Season not found")

    db.query(Season).filter(Season.status == SeasonStatus.active, Season.id != season_id).update(
        {"status": SeasonStatus.complete}, synchronize_session=False
    )
    season.status = SeasonStatus.active
    db.commit()
    db.refresh(season)
    return season


@router.delete("/{season_id}", status_code=204)
def delete_season(
    season_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_commissioner),
):
    """Permanently deletes a season and everything scoped to it -- rosters,
    the queue, and every auction (with its items, bids, and reserve bids).
    Meant for cleaning up old test seasons; there's no undo, so the
    frontend confirms before calling this.

    CribSheetEntry and TeamSeasonResult are deliberately untouched: neither
    is season-scoped (a crib sheet value is a player's opinion of a team in
    general, and historical results are keyed by the real-world league
    season, not this app's Season row)."""
    season = db.get(Season, season_id)
    if season is None:
        raise HTTPException(status_code=404, detail="Season not found")

    auction_ids = [row[0] for row in db.query(Auction.id).filter(Auction.season_id == season_id).all()]
    if auction_ids:
        item_ids = [
            row[0]
            for row in db.query(AuctionItem.id).filter(AuctionItem.auction_id.in_(auction_ids)).all()
        ]
        if item_ids:
            db.query(Bid).filter(Bid.auction_item_id.in_(item_ids)).delete(synchronize_session=False)
            db.query(ReserveBid).filter(ReserveBid.auction_item_id.in_(item_ids)).delete(
                synchronize_session=False
            )
            db.query(AuctionItem).filter(AuctionItem.id.in_(item_ids)).delete(synchronize_session=False)
        db.query(Auction).filter(Auction.id.in_(auction_ids)).delete(synchronize_session=False)

    db.query(QueueEntry).filter(QueueEntry.season_id == season_id).delete(synchronize_session=False)
    db.query(RosterEntry).filter(RosterEntry.season_id == season_id).delete(synchronize_session=False)

    db.delete(season)
    db.commit()
