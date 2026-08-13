import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import Avatar from "../components/Avatar";
import { useAuth } from "../auth/AuthContext";
import { api, type LeagueRules, type RosterEntry, type Season, type User } from "../lib/api";

export default function Roster() {
  const { seasonId } = useParams();
  const { user } = useAuth();
  const [season, setSeason] = useState<Season | null>(null);
  const [entries, setEntries] = useState<RosterEntry[]>([]);
  const [rules, setRules] = useState<LeagueRules | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [rollbackError, setRollbackError] = useState<string | null>(null);

  const loadRoster = () => api.get<RosterEntry[]>(`/seasons/${seasonId}/roster`).then(setEntries);

  useEffect(() => {
    api.get<Season[]>("/seasons").then((seasons) => {
      setSeason(seasons.find((s) => String(s.id) === seasonId) ?? null);
    });
    loadRoster();
    api.get<LeagueRules>("/leagues/rules").then(setRules);
    api.get<User[]>("/users").then(setUsers);
  }, [seasonId]);

  const rollback = async (entry: RosterEntry) => {
    if (!confirm(`Roll back ${entry.team.name} and return it to the pool?`)) return;
    setRollbackError(null);
    try {
      await api.del(`/seasons/${seasonId}/roster/${entry.id}`);
      await loadRoster();
    } catch (e) {
      setRollbackError(e instanceof Error ? e.message : "Failed to roll back");
    }
  };

  const usersById = new Map(users.map((u) => [u.id, u]));

  const byUser = entries.reduce<Record<number, RosterEntry[]>>((acc, e) => {
    (acc[e.user_id] ??= []).push(e);
    return acc;
  }, {});

  const leagueCounts = (rosterEntries: RosterEntry[]) => {
    const counts: Record<string, number> = {};
    for (const e of rosterEntries) {
      counts[e.team.league] = (counts[e.team.league] ?? 0) + 1;
    }
    return counts;
  };

  return (
    <div className="page">
      <h1>{season?.name ?? "Season"} Rosters</h1>
      <p className="inline-form">
        <Link to={`/seasons/${seasonId}/auction/fall`}>Go to fall auction →</Link>
        <Link to={`/seasons/${seasonId}/auction/spring`}>Go to spring auction →</Link>
      </p>
      {Object.entries(byUser).map(([userId, rosterEntries]) => {
        const spent = rosterEntries.reduce((sum, e) => sum + e.price_paid, 0);
        const counts = leagueCounts(rosterEntries);
        const player = usersById.get(Number(userId));
        return (
          <div key={userId} className="roster-block">
            <h2>
              <Link to={`/seasons/${seasonId}/players/${userId}`} className="player-link">
                <Avatar name={player?.display_name ?? `User #${userId}`} src={player?.avatar_data_url} size={28} />
                {userId === String(user?.id) ? "You" : (player?.display_name ?? `User #${userId}`)}
              </Link>{" "}
              <span className="pill">${spent} spent</span>
            </h2>
            {rules && (
              <p className="league-progress">
                {Object.entries(rules.roster_limits).map(([league, limit]) => (
                  <span key={league} className="pill">
                    {league}: {counts[league] ?? 0}/{limit}
                  </span>
                ))}
              </p>
            )}
            <ul>
              {rosterEntries.map((e) => (
                <li key={e.id}>
                  {e.team.league} — {e.team.name} (${e.price_paid})
                  {e.source === "commissioner_correction" && (
                    <span className="pill">corrected</span>
                  )}
                  {user?.is_commissioner && (
                    <button
                      type="button"
                      className="rollback-btn"
                      onClick={() => rollback(e)}
                      title="Undo this pick and return the team to the pool"
                    >
                      Roll back
                    </button>
                  )}
                </li>
              ))}
            </ul>
          </div>
        );
      })}
      {entries.length === 0 && <p>No teams won yet.</p>}
      {rollbackError && <p className="error">{rollbackError}</p>}

      {user?.is_commissioner && (
        <p>
          <Link to="/admin">Commissioner tools →</Link>
        </p>
      )}
    </div>
  );
}
