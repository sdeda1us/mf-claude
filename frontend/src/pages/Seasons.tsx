import { useEffect, useMemo, useState } from "react";
import { useAuth } from "../auth/AuthContext";
import PlayerRosterPanel from "../components/PlayerRosterPanel";
import ScoringSummaryTable from "../components/ScoringSummaryTable";
import { api, type ScoringSummary, type Season, type User } from "../lib/api";

const STATUS_LABEL: Record<Season["status"], string> = {
  setup: "Setup",
  active: "Active",
  complete: "Complete",
};

export default function Seasons() {
  const { user: viewer } = useAuth();
  const [seasons, setSeasons] = useState<Season[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [selectedSeasonId, setSelectedSeasonId] = useState("");
  const [selectedUserId, setSelectedUserId] = useState("");
  const [scoringSummary, setScoringSummary] = useState<ScoringSummary | null>(null);

  useEffect(() => {
    api.get<Season[]>("/seasons").then(setSeasons);
    api.get<User[]>("/users").then(setUsers);
  }, []);

  // Default to the active season the first time seasons load, falling back
  // to the most recent one if none is active.
  useEffect(() => {
    if (selectedSeasonId || seasons.length === 0) return;
    const active = seasons.find((s) => s.status === "active");
    setSelectedSeasonId(String((active ?? seasons[0]).id));
  }, [seasons, selectedSeasonId]);

  useEffect(() => {
    if (!selectedSeasonId) {
      setScoringSummary(null);
      return;
    }
    api.get<ScoringSummary>(`/seasons/${selectedSeasonId}/scoring-summary`).then(setScoringSummary);
  }, [selectedSeasonId]);

  // Default the player picker to whoever's logged in; if that can't be
  // determined, fall back to first place in the standings. Re-applied
  // every time the selected season changes.
  const defaultUserId = useMemo(() => {
    if (viewer) return String(viewer.id);
    if (scoringSummary && scoringSummary.owners.length > 0) {
      return String(scoringSummary.owners[0].user_id);
    }
    return "";
  }, [viewer, scoringSummary]);

  useEffect(() => {
    setSelectedUserId(defaultUserId);
  }, [selectedSeasonId, defaultUserId]);

  return (
    <div className="page page-wide">
      <h1>Seasons</h1>

      <label className="season-picker">
        View season
        <select value={selectedSeasonId} onChange={(e) => setSelectedSeasonId(e.target.value)}>
          {seasons.map((s) => (
            <option key={s.id} value={s.id}>
              {s.name} — {STATUS_LABEL[s.status]}
            </option>
          ))}
        </select>
      </label>

      {seasons.length === 0 && <p>No seasons yet.</p>}

      {selectedSeasonId && (
        <div className="season-columns">
          <div>
            <h2>Standings</h2>
            {scoringSummary === null ? (
              <p className="crib-value-note">Loading…</p>
            ) : scoringSummary.owners.length > 0 ? (
              <ScoringSummaryTable scoringSummary={scoringSummary} users={users} />
            ) : (
              <p className="crib-value-note">No scoring data for this season yet.</p>
            )}
          </div>

          <div>
            <h2>Roster</h2>
            <label className="season-picker">
              Player
              <select value={selectedUserId} onChange={(e) => setSelectedUserId(e.target.value)}>
                {users.map((u) => (
                  <option key={u.id} value={u.id}>
                    {u.display_name}
                  </option>
                ))}
              </select>
            </label>
            {selectedUserId && (
              <PlayerRosterPanel seasonId={selectedSeasonId} userId={selectedUserId} />
            )}
          </div>
        </div>
      )}
    </div>
  );
}
