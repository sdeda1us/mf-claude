import { useEffect, useState } from "react";
import { api, type Season, type Team, type User } from "../lib/api";

export default function Admin() {
  const [seasons, setSeasons] = useState<Season[]>([]);
  const [teams, setTeams] = useState<Team[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [seasonId, setSeasonId] = useState("");
  const [userId, setUserId] = useState("");
  const [teamId, setTeamId] = useState("");
  const [price, setPrice] = useState("");
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    api.get<Season[]>("/seasons").then(setSeasons);
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

  return (
    <div className="page">
      <h1>Commissioner Tools</h1>
      <h2>Manual roster correction</h2>
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
        <button type="submit">Save correction</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}
