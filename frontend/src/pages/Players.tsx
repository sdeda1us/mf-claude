import { useEffect, useState } from "react";
import Avatar from "../components/Avatar";
import PlayerRosterPanel from "../components/PlayerRosterPanel";
import { api, type Season, type User } from "../lib/api";

export default function Players() {
  const [seasons, setSeasons] = useState<Season[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [seasonId, setSeasonId] = useState<string>("");
  const [selectedUserId, setSelectedUserId] = useState<string>("");

  useEffect(() => {
    api.get<Season[]>("/seasons").then((s) => {
      setSeasons(s);
      if (s.length > 0) setSeasonId(String(s[0].id));
    });
    api.get<User[]>("/users").then(setUsers);
  }, []);

  return (
    <div className="page">
      <h1>Players</h1>
      <p>Pick a league member to see their name, email, and roster.</p>

      {seasons.length > 1 && (
        <div className="stacked-form" style={{ maxWidth: 280 }}>
          <label>
            Season
            <select value={seasonId} onChange={(e) => setSeasonId(e.target.value)}>
              {seasons.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name}
                </option>
              ))}
            </select>
          </label>
        </div>
      )}

      <div className="player-picker">
        {users.map((u) => (
          <button
            key={u.id}
            type="button"
            className={String(u.id) === selectedUserId ? "player-picker-item selected" : "player-picker-item"}
            onClick={() => setSelectedUserId(String(u.id))}
          >
            <Avatar name={u.display_name} src={u.avatar_data_url} size={32} />
            {u.display_name}
          </button>
        ))}
      </div>

      {selectedUserId && seasonId && (
        <div className="player-picker-panel">
          <PlayerRosterPanel seasonId={seasonId} userId={selectedUserId} />
        </div>
      )}
    </div>
  );
}
