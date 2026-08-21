import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import { api, type Season } from "../lib/api";

export default function Seasons() {
  const { user } = useAuth();
  const [seasons, setSeasons] = useState<Season[]>([]);
  const [name, setName] = useState("");

  const load = () => api.get<Season[]>("/seasons").then(setSeasons);

  useEffect(() => {
    load();
  }, []);

  const createSeason = async (e: React.FormEvent) => {
    e.preventDefault();
    await api.post("/seasons", { name });
    setName("");
    load();
  };

  return (
    <div className="page">
      <h1>Seasons</h1>
      <ul className="season-list">
        {seasons.map((s) => (
          <li key={s.id}>
            <Link to={`/seasons/${s.id}/roster`}>{s.name}</Link>
            <span className="pill">{s.status}</span>
            <span>
              ${s.fall_budget_per_user} fall / ${s.spring_budget_per_user} spring
            </span>
          </li>
        ))}
      </ul>

      {user?.is_commissioner && (
        <form onSubmit={createSeason} className="inline-form">
          <input
            placeholder="New season name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
          <button type="submit">Create season</button>
        </form>
      )}
    </div>
  );
}
