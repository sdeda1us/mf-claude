import { useEffect, useState } from "react";
import { api, type Season, type Team, type User } from "../lib/api";

const STATUS_LABEL: Record<Season["status"], string> = {
  setup: "Setup",
  active: "Active",
  complete: "Complete",
};

export default function Admin() {
  const [seasons, setSeasons] = useState<Season[]>([]);
  const [teams, setTeams] = useState<Team[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [seasonId, setSeasonId] = useState("");
  const [userId, setUserId] = useState("");
  const [teamId, setTeamId] = useState("");
  const [price, setPrice] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [seasonMessage, setSeasonMessage] = useState<string | null>(null);
  const [seasonActionId, setSeasonActionId] = useState<number | null>(null);

  const loadSeasons = () => {
    api.get<Season[]>("/seasons").then(setSeasons);
  };

  useEffect(() => {
    loadSeasons();
    api.get<Team[]>("/teams").then(setTeams);
    api.get<User[]>("/users").then(setUsers);
  }, []);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage(null);
    try {
      await api.post(`/seasons/${seasonId}/roster/correction`, {
        user_id: Number(userId),
        team_id: Number(teamId),
        price_paid: Number(price),
      });
      setMessage("Roster entry added.");
      setTeamId("");
      setPrice("");
    } catch {
      setMessage("Failed to add roster entry.");
    }
  };

  const activateSeason = async (season: Season) => {
    setSeasonMessage(null);
    setSeasonActionId(season.id);
    try {
      await api.post(`/seasons/${season.id}/activate`);
      setSeasonMessage(`"${season.name}" is now the active season.`);
      loadSeasons();
    } catch {
      setSeasonMessage("Failed to activate that season.");
    } finally {
      setSeasonActionId(null);
    }
  };

  const deleteSeason = async (season: Season) => {
    if (
      !confirm(
        `Permanently delete "${season.name}"? This removes its entire roster, queue, and auction history (every bid, on every team) for everyone. This can't be undone.`
      )
    ) {
      return;
    }
    setSeasonMessage(null);
    setSeasonActionId(season.id);
    try {
      await api.del(`/seasons/${season.id}`);
      setSeasonMessage(`"${season.name}" was deleted.`);
      loadSeasons();
    } catch {
      setSeasonMessage("Failed to delete that season.");
    } finally {
      setSeasonActionId(null);
    }
  };

  return (
    <div className="page">
      <h1>Commissioner Tools</h1>

      <h2>Seasons</h2>
      <div className="crib-add-panel">
        {seasons.length === 0 ? (
          <p className="queue-empty">No seasons yet.</p>
        ) : (
          <table className="sortable-table season-admin-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Status</th>
                <th>Fall budget</th>
                <th>Spring budget</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {seasons.map((s) => (
                <tr key={s.id}>
                  <td>{s.name}</td>
                  <td>
                    <span className={s.status === "active" ? "pill season-active-pill" : "pill"}>
                      {STATUS_LABEL[s.status]}
                    </span>
                  </td>
                  <td>${s.fall_budget_per_user}</td>
                  <td>${s.spring_budget_per_user}</td>
                  <td className="season-admin-actions">
                    <button
                      type="button"
                      disabled={s.status === "active" || seasonActionId === s.id}
                      title={s.status === "active" ? "Already the active season" : "Make this the active season"}
                      onClick={() => activateSeason(s)}
                    >
                      Set active
                    </button>
                    <button
                      type="button"
                      className="rollback-btn"
                      disabled={seasonActionId === s.id}
                      title="Permanently delete this season and everything in it"
                      onClick={() => deleteSeason(s)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
        {seasonMessage && (
          <p className={seasonMessage.startsWith("Failed") ? "error" : "saved-message"}>
            {seasonMessage}
          </p>
        )}
      </div>

      <h2>Manual roster correction</h2>
      <div className="crib-add-panel">
        <form onSubmit={submit} className="stacked-form">
          <label>
            Season
            <select value={seasonId} onChange={(e) => setSeasonId(e.target.value)} required>
              <option value="">Select…</option>
              {seasons.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name}
                </option>
              ))}
            </select>
          </label>
          <label>
            User
            <select value={userId} onChange={(e) => setUserId(e.target.value)} required>
              <option value="">Select…</option>
              {users.map((u) => (
                <option key={u.id} value={u.id}>
                  {u.display_name}
                </option>
              ))}
            </select>
          </label>
          <label>
            Team
            <select value={teamId} onChange={(e) => setTeamId(e.target.value)} required>
              <option value="">Select…</option>
              {teams.map((t) => (
                <option key={t.id} value={t.id}>
                  {t.league} — {t.name}
                </option>
              ))}
            </select>
          </label>
          <label>
            Price paid
            <input
              type="number"
              min="0"
              value={price}
              onChange={(e) => setPrice(e.target.value)}
              required
            />
          </label>
          <button type="submit" className="btn-primary">
            Save correction
          </button>
        </form>
        {message && (
          <p className={message === "Roster entry added." ? "saved-message" : "error"}>{message}</p>
        )}
      </div>
    </div>
  );
}
