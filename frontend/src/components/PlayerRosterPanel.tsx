import { useEffect, useMemo, useState } from "react";
import { useAuth } from "../auth/AuthContext";
import {
  api,
  type ExampleScoreRow,
  type LeagueRules,
  type RosterEntry,
  type Season,
  type User,
} from "../lib/api";
import Avatar from "./Avatar";

interface FilledSlot {
  kind: "filled";
  entry: RosterEntry;
  points: number | null;
}
interface EmptySlot {
  kind: "empty";
  key: string;
}
type Slot = FilledSlot | EmptySlot;

interface PlayerRosterPanelProps {
  seasonId: string;
  userId: string;
}

export default function PlayerRosterPanel({ seasonId, userId }: PlayerRosterPanelProps) {
  const { user: viewer } = useAuth();
  const [season, setSeason] = useState<Season | null>(null);
  const [player, setPlayer] = useState<User | null>(null);
  const [entries, setEntries] = useState<RosterEntry[]>([]);
  const [scores, setScores] = useState<ExampleScoreRow[]>([]);
  const [rules, setRules] = useState<LeagueRules | null>(null);

  useEffect(() => {
    api.get<Season[]>("/seasons").then((seasons) => {
      setSeason(seasons.find((s) => String(s.id) === seasonId) ?? null);
    });
    api.get<User[]>("/users").then((users) => {
      setPlayer(users.find((u) => String(u.id) === userId) ?? null);
    });
    api.get<RosterEntry[]>(`/seasons/${seasonId}/roster`).then(setEntries);
    api.get<ExampleScoreRow[]>("/leagues/example-scores").then(setScores);
    api.get<LeagueRules>("/leagues/rules").then(setRules);
  }, [seasonId, userId]);

  const scoreByTeamId = useMemo(() => new Map(scores.map((s) => [s.team_id, s.points])), [scores]);

  const ownedTeams = useMemo(
    () => entries.filter((e) => String(e.user_id) === userId),
    [entries, userId]
  );

  const leagueGroups = useMemo(() => {
    if (!rules) return [];
    return Object.entries(rules.roster_limits).map(([league, limit]) => {
      const owned: FilledSlot[] = ownedTeams
        .filter((e) => e.team.league === league)
        .map((entry) => ({ kind: "filled", entry, points: scoreByTeamId.get(entry.team.id) ?? null }));
      owned.sort((a, b) => (b.points ?? -1) - (a.points ?? -1));

      const empty: EmptySlot[] = Array.from(
        { length: Math.max(limit - owned.length, 0) },
        (_, i) => ({ kind: "empty", key: `${league}-empty-${i}` })
      );

      const slots: Slot[] = [...owned, ...empty];
      return { league, limit, filledCount: owned.length, slots };
    });
  }, [rules, ownedTeams, scoreByTeamId]);

  const totalSpent = ownedTeams.reduce((sum, e) => sum + e.price_paid, 0);
  const totalPoints = ownedTeams.reduce((sum, e) => sum + (scoreByTeamId.get(e.team.id) ?? 0), 0);
  const totalSlots = rules ? Object.values(rules.roster_limits).reduce((a, b) => a + b, 0) : null;

  if (!season || !player) return <p>Loading…</p>;

  return (
    <div>
      <div className="player-header">
        <Avatar name={player.display_name} src={player.avatar_data_url} size={64} />
        <div>
          <h1>
            {player.display_name}
            {viewer?.id === player.id && <span className="pill">You</span>}
          </h1>
          <p className="connection-status">
            {player.email} &nbsp;·&nbsp; {season.name}
          </p>
        </div>
      </div>

      <div className="summary-strip">
        <div className="summary-stat">
          <span className="summary-value">{ownedTeams.length}</span>
          <span className="summary-label">
            teams owned{totalSlots != null ? ` / ${totalSlots}` : ""}
          </span>
        </div>
        <div className="summary-stat">
          <span className="summary-value">${totalSpent}</span>
          <span className="summary-label">total spent</span>
        </div>
        <div className="summary-stat">
          <span className="summary-value">{totalPoints}</span>
          <span className="summary-label">total prior-season points</span>
        </div>
      </div>

      {leagueGroups.map(({ league, limit, filledCount, slots }) => (
        <div key={league} className="rules-card">
          <div className="ribbon">{league}</div>
          <p className="rules-card-meta">
            <span className="pill">
              {filledCount}/{limit} filled
            </span>
          </p>
          <table>
            <tbody>
              {slots.map((slot) =>
                slot.kind === "filled" ? (
                  <tr key={slot.entry.id}>
                    <td>{slot.entry.team.name}</td>
                    <td className="points-cell">${slot.entry.price_paid}</td>
                    <td className="points-cell">{slot.points ?? "—"}</td>
                  </tr>
                ) : (
                  <tr key={slot.key} className="roster-row-empty">
                    <td>Empty slot</td>
                    <td className="points-cell">—</td>
                    <td className="points-cell">—</td>
                  </tr>
                )
              )}
            </tbody>
          </table>
        </div>
      ))}
    </div>
  );
}
