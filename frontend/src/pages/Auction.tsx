import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import Avatar from "../components/Avatar";
import { useAuth } from "../auth/AuthContext";
import {
  api,
  type Auction,
  type CribSheetEntry,
  type ExampleScoreRow,
  type LeagueRules,
  type QueueEntry,
  type RosterEntry,
  type Team,
  type User,
} from "../lib/api";
import { useAuctionSocket } from "../lib/useAuctionSocket";

type SortKey = "name" | "league" | "points";
type SortDir = "asc" | "desc";

// Must match backend/app/auction_timer.py's NOMINATION_TIMEOUT_SECONDS —
// the actual deadline is server-driven (measured from turn_started_at), this
// is only used client-side to compute the live countdown display.
const NOMINATION_TIMEOUT_SECONDS = 3 * 60 * 60; // 3 hours

// The backend serializes datetimes as UTC with no "Z"/offset suffix (SQLite
// and a plain Postgres TIMESTAMP column both drop tzinfo on round-trip) —
// without forcing UTC here, `new Date(...)` parses it as local time and
// throws any countdown built from it off by the browser's UTC offset.
function parseUtcMs(raw: string): number {
  return Date.parse(/Z|[+-]\d\d:\d\d$/.test(raw) ? raw : `${raw}Z`);
}

function formatCountdown(totalSeconds: number): string {
  const h = Math.floor(totalSeconds / 3600);
  const m = Math.floor((totalSeconds % 3600) / 60);
  const s = totalSeconds % 60;
  if (h > 0) return `${h}h ${m}m ${s}s`;
  if (m > 0) return `${m}m ${s}s`;
  return `${s}s`;
}

export default function AuctionRoom() {
  const { seasonId, session: sessionParam } = useParams();
  const session: "fall" | "spring" = sessionParam === "spring" ? "spring" : "fall";
  const { user } = useAuth();
  const [auction, setAuction] = useState<Auction | null>(null);
  const [teams, setTeams] = useState<Team[]>([]);
  const [scores, setScores] = useState<ExampleScoreRow[]>([]);
  const [roster, setRoster] = useState<RosterEntry[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [rules, setRules] = useState<LeagueRules | null>(null);
  const [bidAmount, setBidAmount] = useState("");
  const [reserveAmount, setReserveAmount] = useState("");
  const [nameFilter, setNameFilter] = useState("");
  const [sportFilter, setSportFilter] = useState("");
  const [showTeamBoard, setShowTeamBoard] = useState(false);
  const [sortKey, setSortKey] = useState<SortKey>("name");
  const [sortDir, setSortDir] = useState<SortDir>("asc");
  const [expandedLeagues, setExpandedLeagues] = useState<Set<string>>(new Set());
  const [scoringModalLeague, setScoringModalLeague] = useState<string | null>(null);
  const [pendingTeam, setPendingTeam] = useState<Team | null>(null);
  const [modalBidAmount, setModalBidAmount] = useState("1");
  const [modalError, setModalError] = useState<string | null>(null);
  const [queue, setQueue] = useState<QueueEntry[]>([]);
  const [cribSheet, setCribSheet] = useState<CribSheetEntry[]>([]);
  const [nowTick, setNowTick] = useState(() => Date.now());
  const [rosterTabUserId, setRosterTabUserId] = useState<number | null>(null);

  useEffect(() => {
    setAuction(null);
    api.get<Auction | null>(`/auctions/seasons/${seasonId}?session=${session}`).then(setAuction);
    api.get<Team[]>("/teams").then(setTeams);
    api.get<ExampleScoreRow[]>("/leagues/example-scores").then(setScores);
    api.get<User[]>("/users").then(setUsers);
    api.get<LeagueRules>("/leagues/rules").then(setRules);
    api.get<CribSheetEntry[]>("/crib-sheet").then(setCribSheet);
  }, [seasonId, session]);

  const { state, error, connected, sendBid, sendPass, sendReserve } = useAuctionSocket(
    auction?.id ?? null
  );

  // Refetch the roster whenever the active item changes (a new nomination,
  // or a sale closing) — that's the authoritative source of which teams are
  // already taken, and roster/state updates can arrive independently.
  useEffect(() => {
    if (!seasonId) return;
    api.get<RosterEntry[]>(`/seasons/${seasonId}/roster`).then(setRoster);
  }, [seasonId, state?.active_item?.id, state?.active_item?.status]);

  const loadQueue = () => {
    if (!seasonId) return;
    api.get<QueueEntry[]>(`/seasons/${seasonId}/queue`).then(setQueue);
  };

  // Refetch on the same triggers as the roster — a sale prunes sold teams
  // out of every queue server-side, so this keeps the queue list in sync.
  useEffect(() => {
    loadQueue();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [seasonId, state?.active_item?.id, state?.active_item?.status]);

  // Ticks once a second so the nomination and bidding countdowns stay live.
  useEffect(() => {
    const id = setInterval(() => setNowTick(Date.now()), 1000);
    return () => clearInterval(id);
  }, []);

  const startAuction = async () => {
    const created = await api.post<Auction>(`/auctions/seasons/${seasonId}?session=${session}`);
    setAuction(created);
  };

  const pauseAuction = async () => {
    if (!auction) return;
    await api.post(`/auctions/${auction.id}/pause`);
  };

  const resumeAuction = async () => {
    if (!auction) return;
    await api.post(`/auctions/${auction.id}/resume`);
  };

  const openBidModal = (team: Team) => {
    setPendingTeam(team);
    setModalBidAmount("1");
    setModalError(null);
  };

  const confirmNominateAndBid = async () => {
    if (!pendingTeam || !auction) return;
    const amount = Number(modalBidAmount);
    if (!amount || amount < 1) {
      setModalError("Enter a bid of at least $1");
      return;
    }
    setModalError(null);
    try {
      await api.post(`/auctions/${auction.id}/nominate`, { team_id: pendingTeam.id });
      sendBid(amount);
      setPendingTeam(null);
    } catch (e) {
      setModalError(e instanceof Error ? e.message : "Failed to nominate");
    }
  };

  const closeItem = async () => {
    if (!auction) return;
    await api.post(`/auctions/${auction.id}/close`);
  };

  const cancelNomination = async () => {
    if (!auction) return;
    if (!confirm("Cancel this nomination? Any bids on it will be removed and the turn will go back to whoever nominated it.")) {
      return;
    }
    await api.post(`/auctions/${auction.id}/cancel-nomination`);
  };

  const forceTurn = async (userId: number) => {
    if (!auction) return;
    await api.post(`/auctions/${auction.id}/force-turn`, { user_id: userId });
  };

  const bid = (e: React.FormEvent) => {
    e.preventDefault();
    const amount = Number(bidAmount);
    if (amount > 0) sendBid(amount);
    setBidAmount("");
  };

  const lockReserve = (e: React.FormEvent) => {
    e.preventDefault();
    const amount = Number(reserveAmount);
    if (amount > 0) sendReserve(true, amount);
    setReserveAmount("");
  };

  const unlockReserve = () => sendReserve(false);

  const addToQueue = async (team: Team) => {
    if (!seasonId) return;
    await api.post(`/seasons/${seasonId}/queue`, { team_id: team.id });
    loadQueue();
  };

  const removeFromQueue = async (entryId: number) => {
    if (!seasonId) return;
    await api.del(`/seasons/${seasonId}/queue/${entryId}`);
    loadQueue();
  };

  const moveQueueEntry = async (entryId: number, direction: "up" | "down") => {
    if (!seasonId) return;
    const updated = await api.post<QueueEntry[]>(
      `/seasons/${seasonId}/queue/${entryId}/move`,
      { direction }
    );
    setQueue(updated);
  };

  const usersById = useMemo(() => new Map(users.map((u) => [u.id, u])), [users]);
  const soldTeamIds = useMemo(() => new Set(roster.map((r) => r.team.id)), [roster]);
  const scoreByTeamId = useMemo(() => new Map(scores.map((s) => [s.team_id, s.points])), [scores]);
  const cribValueByTeamId = useMemo(
    () => new Map(cribSheet.map((e) => [e.team_id, e.value])),
    [cribSheet]
  );
  const queuedTeamIds = useMemo(() => new Set(queue.map((q) => q.team.id)), [queue]);

  // How many teams in this league it'll take for every player to fill out
  // their roster there — each player's own cap times the number of
  // players — not the size of the real-world pool (a small-cap league in a
  // huge pool, e.g. NCAAMB, would otherwise show a denominator nobody's
  // ever going to reach).
  const neededByLeague = useMemo(() => {
    if (!rules) return {};
    const counts: Record<string, number> = {};
    for (const [league, limit] of Object.entries(rules.roster_limits)) {
      counts[league] = limit * users.length;
    }
    return counts;
  }, [rules, users]);

  const soldByLeague = useMemo(() => {
    const grouped: Record<string, RosterEntry[]> = {};
    for (const entry of roster) {
      (grouped[entry.team.league] ??= []).push(entry);
    }
    for (const entries of Object.values(grouped)) {
      entries.sort((a, b) => b.price_paid - a.price_paid);
    }
    return grouped;
  }, [roster]);

  const rosterByUserId = useMemo(() => {
    const grouped: Record<number, RosterEntry[]> = {};
    for (const entry of roster) {
      (grouped[entry.user_id] ??= []).push(entry);
    }
    for (const entries of Object.values(grouped)) {
      entries.sort((a, b) => a.team.league.localeCompare(b.team.league) || a.team.name.localeCompare(b.team.name));
    }
    return grouped;
  }, [roster]);

  const toggleLeague = (league: string) => {
    setExpandedLeagues((prev) => {
      const next = new Set(prev);
      if (next.has(league)) next.delete(league);
      else next.add(league);
      return next;
    });
  };

  const toggleSort = (key: SortKey) => {
    if (key === sortKey) {
      setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    } else {
      setSortKey(key);
      setSortDir(key === "points" ? "desc" : "asc");
    }
  };
  const arrow = (key: SortKey) => (sortKey === key ? (sortDir === "asc" ? " ▲" : " ▼") : "");

  // Each league belongs to exactly one auction session — see
  // docs/wiki/README.md's "Auction Sessions" section — so this auction page
  // only ever deals in this session's leagues, not the full 19.
  const sessionTeams = useMemo(() => {
    if (!rules) return [];
    return teams.filter((t) => rules.league_session[t.league] === session);
  }, [teams, rules, session]);

  const sports = useMemo(
    () => Array.from(new Set(sessionTeams.map((t) => t.sport))).sort(),
    [sessionTeams]
  );

  const board = useMemo(() => {
    const rows = sessionTeams
      .filter((t) => !soldTeamIds.has(t.id))
      .filter((t) => t.name.toLowerCase().includes(nameFilter.toLowerCase()))
      .filter((t) => !sportFilter || t.sport === sportFilter)
      .map((t) => ({
        team: t,
        points: scoreByTeamId.get(t.id) ?? null,
        cribValue: cribValueByTeamId.get(t.id) ?? null,
      }));
    rows.sort((a, b) => {
      let cmp: number;
      if (sortKey === "points") cmp = (a.points ?? -1) - (b.points ?? -1);
      else if (sortKey === "league") cmp = a.team.league.localeCompare(b.team.league);
      else cmp = a.team.name.localeCompare(b.team.name);
      return sortDir === "asc" ? cmp : -cmp;
    });
    return rows;
  }, [sessionTeams, soldTeamIds, nameFilter, sportFilter, scoreByTeamId, cribValueByTeamId, sortKey, sortDir]);

  const sessionLabel = session === "fall" ? "Fall" : "Spring";
  const sessionTabs = (
    <div className="session-tabs">
      <Link
        to={`/seasons/${seasonId}/auction/fall`}
        className={session === "fall" ? "session-tab current" : "session-tab"}
      >
        Fall Auction
      </Link>
      <Link
        to={`/seasons/${seasonId}/auction/spring`}
        className={session === "spring" ? "session-tab current" : "session-tab"}
      >
        Spring Auction
      </Link>
    </div>
  );

  if (!auction) {
    return (
      <div className="page">
        {sessionTabs}
        <h1>{sessionLabel} Auction</h1>
        {user?.is_commissioner ? (
          <button onClick={startAuction}>Start the {sessionLabel.toLowerCase()} auction for this season</button>
        ) : (
          <p>The commissioner hasn't started the {sessionLabel.toLowerCase()} auction yet.</p>
        )}
      </div>
    );
  }

  const item = state?.active_item;
  const isPaused = state?.auction.is_paused ?? auction.is_paused;
  const highBid = item?.bids.length ? Math.max(...item.bids.map((b) => b.amount)) : 0;
  const highBidder = item?.bids.length
    ? item.bids.reduce((best, b) => (b.amount > best.amount ? b : best))
    : null;
  const isHighBidder = !!user && !!highBidder && highBidder.user_id === user.id;
  const hasPassed = !!user && !!item?.passed_user_ids.includes(user.id);
  const passedUsers = (item?.passed_user_ids ?? []).map((uid) => ({
    uid,
    name: usersById.get(uid)?.display_name ?? `User #${uid}`,
  }));
  const bidSecondsRemaining = item?.bid_deadline
    ? Math.max(0, Math.floor((parseUtcMs(item.bid_deadline) - nowTick) / 1000))
    : null;

  const currentTurnUserId = state?.current_turn_user_id ?? null;
  const currentTurnUser = currentTurnUserId != null ? usersById.get(currentTurnUserId) : null;
  const isMyTurn = !!user && currentTurnUserId === user.id;
  const canNominate = !item && !isPaused && (user?.is_commissioner || isMyTurn);

  const nominatedByUserId =
    item && auction.nomination_order.length > 0
      ? auction.nomination_order[item.order % auction.nomination_order.length]
      : null;
  const nominatedByUser = nominatedByUserId != null ? usersById.get(nominatedByUserId) : null;

  const turnStartedAtRaw = state?.auction.turn_started_at ?? auction.turn_started_at;
  const secondsRemaining = Math.max(
    0,
    NOMINATION_TIMEOUT_SECONDS - Math.floor((nowTick - parseUtcMs(turnStartedAtRaw)) / 1000)
  );

  const rosterStatuses = state?.roster_status_by_user ?? {};
  const totalBudgetRemaining = Object.values(rosterStatuses).reduce(
    (sum, s) => sum + s.budget_remaining,
    0
  );
  const totalSpotsRemaining = Object.values(rosterStatuses).reduce(
    (sum, s) => sum + s.spots_remaining,
    0
  );

  const activeRosterUserId =
    rosterTabUserId ?? user?.id ?? auction.nomination_order[0] ?? null;
  const activeRosterEntries = activeRosterUserId != null ? rosterByUserId[activeRosterUserId] ?? [] : [];

  return (
    <div className="page page-wide">
      {sessionTabs}
      <div className="auction-header">
        <h1>{sessionLabel} Auction Room</h1>
        {user?.is_commissioner && (
          <button
            type="button"
            className={isPaused ? "btn-success pause-btn" : "btn-primary pause-btn"}
            onClick={isPaused ? resumeAuction : pauseAuction}
          >
            {isPaused ? "Resume Auction" : "Pause Auction"}
          </button>
        )}
      </div>
      <p className="connection-status">
        <span className={connected ? "status-dot" : "status-dot warn"} aria-hidden="true" />
        {connected ? "live" : "reconnecting…"}
      </p>
      {isPaused && (
        <p className="paused-banner">⏸ Auction paused by the commissioner — nominating and bidding are on hold.</p>
      )}

      <ol className="turn-strip">
        {auction.nomination_order.map((uid) => {
          const u = usersById.get(uid);
          const status = rosterStatuses[uid];
          return (
            <li
              key={uid}
              className={
                uid === currentTurnUserId
                  ? uid === user?.id
                    ? "turn-pill current self"
                    : "turn-pill current"
                  : uid === user?.id
                    ? "turn-pill self"
                    : "turn-pill"
              }
            >
              <Link to={`/seasons/${seasonId}/players/${uid}`} className="turn-pill-name player-link">
                <Avatar name={u?.display_name ?? `User #${uid}`} src={u?.avatar_data_url} size={20} />
                {u?.display_name ?? `User #${uid}`}
              </Link>
              {status && (
                <div className="turn-pill-stats">
                  <span>${status.budget_remaining.toFixed(0)} left</span>
                  <span>
                    {status.spots_filled}/{status.spots_filled + status.spots_remaining} spots
                  </span>
                  <span>max ${status.max_bid.toFixed(0)}</span>
                </div>
              )}
              {user?.is_commissioner && !item && uid !== currentTurnUserId && (
                <button
                  type="button"
                  className="force-turn-btn"
                  title={`Force it to be ${u?.display_name ?? `User #${uid}`}'s turn to nominate`}
                  onClick={() => forceTurn(uid)}
                >
                  Make it their turn
                </button>
              )}
            </li>
          );
        })}
      </ol>

      <div className="summary-strip">
        <div className="summary-stat">
          <span className="summary-value">${totalBudgetRemaining.toFixed(0)}</span>
          <span className="summary-label">total $ remaining, all players</span>
        </div>
        <div className="summary-stat">
          <span className="summary-value">{totalSpotsRemaining}</span>
          <span className="summary-label">total open roster spots</span>
        </div>
      </div>

      <div className="auction-layout">
      <div className="auction-main">
        {item ? (
          <div className="on-the-clock has-item">
            <div className="ribbon">Live · Up For Bid</div>
            <div className="badge">{item.team.league}</div>
            <div className="nameplate">{item.team.name}</div>
            <div style={{ marginTop: 8 }}>
              <span className="pill" style={{ marginLeft: 0 }}>
                {item.team.sport}
              </span>
            </div>
            {cribValueByTeamId.get(item.team.id) != null && (
              <p className="crib-value-note">
                Your crib sheet value: <strong>${cribValueByTeamId.get(item.team.id)}</strong>
              </p>
            )}
            <p className="high-bid">
              Current high bid: <strong>${highBid}</strong>
              {highBidder && ` — ${usersById.get(highBidder.user_id)?.display_name ?? `User #${highBidder.user_id}`}`}
            </p>
            {isPaused ? (
              <p className="turn-countdown">Paused</p>
            ) : (
              bidSecondsRemaining !== null && (
                <p className={bidSecondsRemaining <= 5 ? "turn-countdown urgent" : "turn-countdown"}>
                  {formatCountdown(bidSecondsRemaining)} left to bid
                  {bidSecondsRemaining === 0 && " — closing…"}
                </p>
              )
            )}
            <ul className="bid-log">
              {item.bids
                .slice()
                .reverse()
                .map((b) => (
                  <li key={b.id}>
                    {usersById.get(b.user_id)?.display_name ?? `User #${b.user_id}`} bid ${b.amount}
                  </li>
                ))}
            </ul>
            {hasPassed && (
              <p className="turn-countdown">
                You've passed on this team — you can't bid on it again.
              </p>
            )}
            <form onSubmit={bid} className="inline-form">
              <input
                type="number"
                min={highBid + 1}
                placeholder={`> $${highBid}`}
                value={bidAmount}
                onChange={(e) => setBidAmount(e.target.value)}
                disabled={isPaused || hasPassed}
              />
              <button type="submit" className="btn-primary" disabled={isPaused || hasPassed}>
                Bid
              </button>
              {!isHighBidder && !hasPassed && (
                <button
                  type="button"
                  className="pass-btn"
                  disabled={isPaused}
                  title="Declare you're out of bidding on this team"
                  onClick={sendPass}
                >
                  Pass
                </button>
              )}
            </form>

            {!hasPassed && (
              <div className="reserve-panel">
                <p
                  className="reserve-label"
                  title="Lock a max amount and we'll automatically bid $1 over anyone who outbids you, up to that amount, until you win it or the reserve is reached. Only you can see it."
                >
                  Reserve bid
                </p>
                {item.my_reserve?.active ? (
                  <p className="inline-form">
                    Locked at <strong>${item.my_reserve.amount}</strong>
                    <button type="button" onClick={unlockReserve} disabled={isPaused}>
                      Unlock
                    </button>
                  </p>
                ) : (
                  <form onSubmit={lockReserve} className="inline-form">
                    <input
                      type="number"
                      min={highBid + 1}
                      placeholder={`> $${highBid}`}
                      value={reserveAmount}
                      onChange={(e) => setReserveAmount(e.target.value)}
                      disabled={isPaused}
                    />
                    <button type="submit" className="btn-success" disabled={isPaused}>
                      Lock
                    </button>
                  </form>
                )}
              </div>
            )}
            {error && <p className="error">{error}</p>}
            {user?.is_commissioner && (
              <div className="commissioner-controls">
                <button onClick={closeItem}>Close item / sell</button>
                <button
                  type="button"
                  className="rollback-btn"
                  onClick={cancelNomination}
                  title={
                    nominatedByUser
                      ? `Undo this nomination and return the turn to ${nominatedByUser.display_name}`
                      : "Undo this nomination"
                  }
                >
                  Cancel nomination
                  {nominatedByUser && ` (return turn to ${nominatedByUser.display_name})`}
                </button>
              </div>
            )}
            {passedUsers.length > 0 && (
              <div className="passed-pills">
                {passedUsers.map((p) => (
                  <span key={p.uid} className="pill passed-pill">
                    {p.name} passes
                  </span>
                ))}
              </div>
            )}
          </div>
        ) : (
          <div className="on-the-clock on-the-clock-empty">
            {isMyTurn ? (
              <p>
                <strong>It's your turn</strong> — pick a team from the board below to put it up
                for bid.
              </p>
            ) : (
              <p>
                Waiting for <strong>{currentTurnUser?.display_name ?? "the next player"}</strong>{" "}
                to nominate a team.
              </p>
            )}
            {isPaused ? (
              <p className="turn-countdown">Paused</p>
            ) : (
              <p className={secondsRemaining <= 5 ? "turn-countdown urgent" : "turn-countdown"}>
                {formatCountdown(secondsRemaining)} to nominate
                {secondsRemaining === 0 && " — auto-nominating from the queue…"}
              </p>
            )}
          </div>
        )}

        <div className="queue-panel">
          <h2>Your Queue</h2>
          {queue.length === 0 ? (
            <p className="queue-empty">
              Nothing queued yet — use the Queue button below to line up teams. If your turn
              runs out, the top of your queue gets auto-nominated with a $1 bid.
            </p>
          ) : (
            <ol className="queue-list">
              {queue.map((entry, idx) => (
                <li key={entry.id} className="queue-item">
                  <span className="queue-item-team">{entry.team.name}</span>
                  <span className="pill">{entry.team.league}</span>
                  <div className="queue-item-actions">
                    <button
                      type="button"
                      className="queue-move-btn"
                      disabled={idx === 0}
                      title="Move up"
                      onClick={() => moveQueueEntry(entry.id, "up")}
                    >
                      ▲
                    </button>
                    <button
                      type="button"
                      className="queue-move-btn"
                      disabled={idx === queue.length - 1}
                      title="Move down"
                      onClick={() => moveQueueEntry(entry.id, "down")}
                    >
                      ▼
                    </button>
                    {!item && !isPaused && isMyTurn && rules?.league_session[entry.team.league] === session && (
                      <button
                        type="button"
                        className="btn-success queue-bid-btn"
                        onClick={() => openBidModal(entry.team)}
                      >
                        Bid
                      </button>
                    )}
                    <button
                      type="button"
                      className="rollback-btn"
                      title="Remove from queue"
                      onClick={() => removeFromQueue(entry.id)}
                    >
                      Remove
                    </button>
                  </div>
                </li>
              ))}
            </ol>
          )}
        </div>

        <button type="button" onClick={() => setShowTeamBoard((v) => !v)}>
          {showTeamBoard ? "Hide" : "Browse"} all teams
        </button>

        {showTeamBoard && (
          <>
            <div className="team-board-controls">
              <input
                type="text"
                placeholder="Filter by team name…"
                value={nameFilter}
                onChange={(e) => setNameFilter(e.target.value)}
              />
              <select value={sportFilter} onChange={(e) => setSportFilter(e.target.value)}>
                <option value="">All sports</option>
                {sports.map((s) => (
                  <option key={s} value={s}>
                    {s}
                  </option>
                ))}
              </select>
            </div>

            <table className="sortable-table team-board">
              <thead>
                <tr>
                  <th onClick={() => toggleSort("name")}>Team{arrow("name")}</th>
                  <th onClick={() => toggleSort("league")}>League / Sport{arrow("league")}</th>
                  <th onClick={() => toggleSort("points")}>Prior season points{arrow("points")}</th>
                  <th>Your Value</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {board.map(({ team, points, cribValue }) => {
                  const queued = queuedTeamIds.has(team.id);
                  return (
                    <tr key={team.id} className={canNominate ? "team-row" : "team-row disabled"}>
                      <td>{team.name}</td>
                      <td>
                        <span className="pill">{team.league}</span> {team.sport}
                      </td>
                      <td className="points-cell">{points ?? "—"}</td>
                      <td className="points-cell">{cribValue ?? ""}</td>
                      <td className="team-row-actions">
                        <button
                          type="button"
                          className="btn-success team-action-btn"
                          disabled={!canNominate}
                          title={
                            canNominate
                              ? "Nominate this team and place your opening bid"
                              : item
                                ? "An item is already up for bid"
                                : "Not your turn to nominate"
                          }
                          onClick={() => openBidModal(team)}
                        >
                          Bid
                        </button>
                        <button
                          type="button"
                          className="team-action-btn"
                          disabled={queued}
                          title={queued ? "Already in your queue" : "Add to your queue"}
                          onClick={() => addToQueue(team)}
                        >
                          {queued ? "Queued" : "Queue"}
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </>
        )}
      </div>

      <aside className="league-sidebar">
        <div className="rosters-panel">
          <h2>Rosters</h2>
          <div className="roster-tabs">
            {auction.nomination_order.map((uid) => {
              const u = usersById.get(uid);
              return (
                <button
                  key={uid}
                  type="button"
                  className={activeRosterUserId === uid ? "roster-tab current" : "roster-tab"}
                  onClick={() => setRosterTabUserId(uid)}
                  title={u?.display_name ?? `User #${uid}`}
                >
                  <Avatar name={u?.display_name ?? `User #${uid}`} src={u?.avatar_data_url} size={18} />
                  {u?.display_name ?? `User #${uid}`}
                </button>
              );
            })}
          </div>
          <ul className="roster-tab-list">
            {activeRosterEntries.length === 0 ? (
              <li className="league-sold-empty">No teams yet.</li>
            ) : (
              activeRosterEntries.map((entry) => (
                <li key={entry.id}>
                  <span className="league-sold-team">{entry.team.name}</span>
                  <span className="pill">{entry.team.league}</span>
                  <span className="league-sold-price">${entry.price_paid}</span>
                </li>
              ))
            )}
          </ul>
        </div>

        <h2>Leagues</h2>
        {rules &&
          Object.keys(rules.roster_limits)
            .filter((league) => rules.league_session[league] === session)
            .map((league) => {
            const sold = soldByLeague[league] ?? [];
            const needed = neededByLeague[league] ?? 0;
            const spent = sold.reduce((sum, e) => sum + e.price_paid, 0);
            const expanded = expandedLeagues.has(league);
            return (
              <div key={league} className="league-block">
                <div className="league-row">
                  <button
                    type="button"
                    className="league-caret"
                    onClick={() => toggleLeague(league)}
                    aria-expanded={expanded}
                    title={expanded ? "Collapse" : "Expand"}
                  >
                    <span className={expanded ? "caret-icon open" : "caret-icon"}>▸</span>
                    <span className="league-name">{league}</span>
                  </button>
                  <button
                    type="button"
                    className="league-info-btn"
                    onClick={() => setScoringModalLeague(league)}
                    title={`${league} scoring rules`}
                  >
                    ?
                  </button>
                  <div className="league-row-stats">
                    <span>
                      {sold.length}/{needed} taken
                    </span>
                    <span>${spent} spent</span>
                  </div>
                </div>
                {expanded && (
                  <ul className="league-sold-list">
                    {sold.length === 0 && <li className="league-sold-empty">No teams sold yet.</li>}
                    {sold.map((entry) => {
                      const buyer = usersById.get(entry.user_id);
                      return (
                        <li key={entry.id}>
                          <span className="league-sold-team">{entry.team.name}</span>
                          <span className="league-sold-price">${entry.price_paid}</span>
                          <span className="league-sold-buyer">
                            {buyer?.display_name ?? `User #${entry.user_id}`}
                          </span>
                        </li>
                      );
                    })}
                  </ul>
                )}
              </div>
            );
          })}
      </aside>
      </div>

      {scoringModalLeague && rules && (
        <div className="modal-backdrop" onClick={() => setScoringModalLeague(null)}>
          <div className="modal-card rules-card" onClick={(e) => e.stopPropagation()}>
            <div className="ribbon">{scoringModalLeague}</div>
            <button
              type="button"
              className="modal-close"
              onClick={() => setScoringModalLeague(null)}
              aria-label="Close"
            >
              ×
            </button>
            <table>
              <tbody>
                {rules.scoring_rules[scoringModalLeague]?.map((line) => (
                  <tr key={line.label}>
                    <td>{line.label}</td>
                    <td className="points-cell">{line.points > 0 ? `+${line.points}` : line.points}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {pendingTeam && (
        <div className="modal-backdrop" onClick={() => setPendingTeam(null)}>
          <div className="modal-card rules-card bid-confirm-modal" onClick={(e) => e.stopPropagation()}>
            <div className="ribbon">{pendingTeam.league}</div>
            <button
              type="button"
              className="modal-close"
              onClick={() => setPendingTeam(null)}
              aria-label="Close"
            >
              ×
            </button>
            <div className="nameplate">{pendingTeam.name}</div>
            <div style={{ marginTop: 8 }}>
              <span className="pill" style={{ marginLeft: 0 }}>
                {pendingTeam.sport}
              </span>
            </div>
            <p className="bid-confirm-prompt">Nominate this team and place your opening bid?</p>
            <label className="bid-confirm-amount">
              Bid amount
              <input
                type="number"
                min={1}
                autoFocus
                value={modalBidAmount}
                onChange={(e) => setModalBidAmount(e.target.value)}
              />
            </label>
            {modalError && <p className="error">{modalError}</p>}
            <div className="bid-confirm-actions">
              <button type="button" className="btn-success" onClick={confirmNominateAndBid}>
                Bid
              </button>
              <button type="button" onClick={() => setPendingTeam(null)}>
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
