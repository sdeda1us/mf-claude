import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Avatar from "../components/Avatar";
import { api, type LeagueRules, type RosterEntry, type Season, type Team, type User } from "../lib/api";

interface SeasonSnapshot {
  season: Season;
  rows: { user: User; spent: number; teamsDrafted: number }[];
}

export default function Home() {
  const [seasons, setSeasons] = useState<Season[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [rules, setRules] = useState<LeagueRules | null>(null);
  const [teams, setTeams] = useState<Team[]>([]);
  const [snapshots, setSnapshots] = useState<SeasonSnapshot[]>([]);

  useEffect(() => {
    api.get<Season[]>("/seasons").then(setSeasons);
    api.get<User[]>("/users").then(setUsers);
    api.get<LeagueRules>("/leagues/rules").then(setRules);
    api.get<Team[]>("/teams").then(setTeams);
  }, []);

  useEffect(() => {
    const activeSeasons = seasons.filter((s) => s.status === "active");
    if (activeSeasons.length === 0 || users.length === 0) {
      setSnapshots([]);
      return;
    }
    Promise.all(
      activeSeasons.map((season) =>
        api.get<RosterEntry[]>(`/seasons/${season.id}/roster`).then((entries) => {
          const byUser = new Map<number, { spent: number; teamsDrafted: number }>();
          for (const e of entries) {
            const cur = byUser.get(e.user_id) ?? { spent: 0, teamsDrafted: 0 };
            cur.spent += e.price_paid;
            cur.teamsDrafted += 1;
            byUser.set(e.user_id, cur);
          }
          const rows = users
            .map((user) => ({
              user,
              spent: byUser.get(user.id)?.spent ?? 0,
              teamsDrafted: byUser.get(user.id)?.teamsDrafted ?? 0,
            }))
            .sort((a, b) => b.spent - a.spent || b.teamsDrafted - a.teamsDrafted);
          return { season, rows };
        })
      )
    ).then(setSnapshots);
  }, [seasons, users]);

  const leagueCount = rules ? Object.keys(rules.roster_limits).length : null;
  const totalRosterSlots = rules
    ? Object.values(rules.roster_limits).reduce((a, b) => a + b, 0)
    : null;

  return (
    <div className="page page-wide">
      <section className="landing-hero">
        <h1>Welcome to MegaFantasy</h1>
        <p>
          MegaFantasy is a private auction fantasy league for the six of you. Instead of drafting
          individual athletes, you bid real dollars in a live auction for entire teams — across
          MLB, NFL, NBA, NHL, EPL, college football and basketball, tennis, golf, F1, and more —
          and score points based on how those teams actually perform in the real world.
        </p>
        <div className="summary-strip">
          <div className="summary-stat">
            <span className="summary-value">{leagueCount ?? "—"}</span>
            <span className="summary-label">sports leagues</span>
          </div>
          <div className="summary-stat">
            <span className="summary-value">{teams.length || "—"}</span>
            <span className="summary-label">draftable teams</span>
          </div>
          <div className="summary-stat">
            <span className="summary-value">{totalRosterSlots ?? "—"}</span>
            <span className="summary-label">roster slots per player</span>
          </div>
          <div className="summary-stat">
            <span className="summary-value">{users.length || 6}</span>
            <span className="summary-label">league members</span>
          </div>
        </div>

        <div className="hero-gallery">
          <div className="hero-gallery-item">
            <img src="/images/nfl.webp" alt="NFL running back breaking a tackle" />
            <span className="pill hero-gallery-label">NFL</span>
          </div>
          <div className="hero-gallery-item">
            <img src="/images/wnba.webp" alt="WNBA guard driving past a defender" />
            <span className="pill hero-gallery-label">WNBA</span>
          </div>
          <div className="hero-gallery-item">
            <img src="/images/tennis.webp" alt="Tennis player stretching for a backhand" />
            <span className="pill hero-gallery-label">Tennis</span>
          </div>
          <div className="hero-gallery-item">
            <img src="/images/rugby.webp" alt="Rugby scrum" />
            <span className="pill hero-gallery-label">URC</span>
          </div>
        </div>
      </section>

      <section>
        <h2>Active Season</h2>
        {snapshots.length === 0 ? (
          <p>
            No season is currently active. <Link to="/seasons">See all seasons →</Link>
          </p>
        ) : (
          snapshots.map(({ season, rows }) => (
            <div key={season.id} className="rules-card">
              <div className="ribbon">{season.name}</div>
              <p className="rules-card-meta">
                <span className="pill">${season.budget_per_user} budget</span>
              </p>
              <table className="sortable-table">
                <thead>
                  <tr>
                    <th>Player</th>
                    <th>Teams drafted</th>
                    <th>$ Spent</th>
                  </tr>
                </thead>
                <tbody>
                  {rows.map(({ user, spent, teamsDrafted }) => (
                    <tr key={user.id}>
                      <td>
                        <span className="player-link">
                          <Avatar name={user.display_name} src={user.avatar_data_url} size={22} />
                          {user.display_name}
                        </span>
                      </td>
                      <td className="points-cell">{teamsDrafted}</td>
                      <td className="points-cell">${spent}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <p className="crib-value-note">
                This is a draft-activity snapshot, not performance-based standings — real-world
                scoring for the active season isn't wired up yet. Once it is, this table will
                rank by points instead.
              </p>
              <p className="inline-form">
                <Link to={`/seasons/${season.id}/roster`}>View full roster →</Link>
                <Link to={`/seasons/${season.id}/auction/fall`}>Go to fall auction →</Link>
                <Link to={`/seasons/${season.id}/auction/spring`}>Go to spring auction →</Link>
              </p>
            </div>
          ))
        )}
      </section>

      <section>
        <h2>Your League</h2>
        <div className="player-picker">
          {users.map((u) => (
            <span key={u.id} className="player-picker-item">
              <Avatar name={u.display_name} src={u.avatar_data_url} size={28} />
              {u.display_name}
              {u.is_commissioner && <span className="pill">Commish</span>}
            </span>
          ))}
        </div>
        <p>
          <Link to="/players">View player profiles →</Link>
        </p>
      </section>

      <section>
        <h2>Explore</h2>
        <p className="inline-form">
          <Link to="/rules">Scoring rules →</Link>
          <Link to="/crib-sheet">Your crib sheet →</Link>
          <Link to="/example-scores">Example scores →</Link>
          <Link to="/seasons">All seasons →</Link>
        </p>
      </section>
    </div>
  );
}
