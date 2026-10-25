import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Avatar from "../components/Avatar";
import TodaysGamesCard from "../components/TodaysGamesCard";
import YesterdaysResultsCard from "../components/YesterdaysResultsCard";
import "../topps-theme.css";
import {
  api,
  type RosterEntry,
  type ScoringSummary,
  type Season,
  type TodaysGame,
  type User,
  type YesterdaysResult,
} from "../lib/api";

interface SeasonSnapshot {
  season: Season;
  rows: { user: User; spent: number; teamsDrafted: number }[];
  scoringSummary: ScoringSummary;
  todaysGames: TodaysGame[];
  yesterdaysResults: YesterdaysResult[];
}

export default function HomeTopps() {
  const [seasons, setSeasons] = useState<Season[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [snapshots, setSnapshots] = useState<SeasonSnapshot[]>([]);

  useEffect(() => {
    api.get<Season[]>("/seasons").then(setSeasons);
    api.get<User[]>("/users").then(setUsers);
  }, []);

  useEffect(() => {
    const activeSeasons = seasons.filter((s) => s.status === "active");
    if (activeSeasons.length === 0 || users.length === 0) {
      setSnapshots([]);
      return;
    }
    Promise.all(
      activeSeasons.map((season) =>
        Promise.all([
          api.get<RosterEntry[]>(`/seasons/${season.id}/roster`),
          api.get<ScoringSummary>(`/seasons/${season.id}/scoring-summary`),
          api.get<TodaysGame[]>(`/seasons/${season.id}/todays-games`),
          api.get<YesterdaysResult[]>(`/seasons/${season.id}/yesterdays-results`),
        ]).then(([entries, scoringSummary, todaysGames, yesterdaysResults]) => {
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
          return { season, rows, scoringSummary, todaysGames, yesterdaysResults };
        })
      )
    ).then(setSnapshots);
  }, [seasons, users]);

  return (
    <div className="topps-page">
      <div className="topps-deck">
        <div className="topps-card">
          {/* ---- card front: hero ---- */}
          <div className="topps-front">
            <div className="topps-front-photo">
              <span className="topps-eyebrow">Private Auction League</span>
              <h1 className="topps-wordmark">
                MEGA
                <br />
                FANTASY
              </h1>
            </div>
            <div className="topps-stripe">
              <span>Fantasy Auction League</span>
            </div>
          </div>

          <div className="topps-pack">
            <div className="topps-pack-card">
              <div className="topps-pack-photo">
                <img src="/images/nfl.webp" alt="NFL running back breaking a tackle" />
              </div>
              <div className="topps-pack-label">NFL</div>
            </div>
            <div className="topps-pack-card">
              <div className="topps-pack-photo">
                <img src="/images/wnba.webp" alt="WNBA guard driving past a defender" />
              </div>
              <div className="topps-pack-label">WNBA</div>
            </div>
            <div className="topps-pack-card">
              <div className="topps-pack-photo">
                <img src="/images/tennis.webp" alt="Tennis player stretching for a backhand" />
              </div>
              <div className="topps-pack-label">Tennis</div>
            </div>
            <div className="topps-pack-card">
              <div className="topps-pack-photo">
                <img src="/images/rugby.webp" alt="Rugby scrum" />
              </div>
              <div className="topps-pack-label">URC</div>
            </div>
          </div>

          {/* ---- card back(s): active season ---- */}
          {snapshots.length === 0 ? (
            <div className="topps-back">
              <div className="topps-card-no">№ 1</div>
              <h2>Active Season Record</h2>
              <p className="topps-empty-season">
                No season is currently active. <Link to="/seasons">See all seasons →</Link>
              </p>
            </div>
          ) : (
            snapshots.map(({ season, rows, scoringSummary, todaysGames, yesterdaysResults }, i) => (
              <div className="topps-back" key={season.id}>
                <div className="topps-card-no">№ {i + 1}</div>
                <h2>{season.name}</h2>
                <p className="topps-season-name">Active Season Record</p>

                <div className="todays-and-yesterday-row topps-games-row">
                  <TodaysGamesCard games={todaysGames} />
                  <YesterdaysResultsCard results={yesterdaysResults} />
                </div>

                <div className="topps-cta-row">
                  <Link className="topps-cta-primary" to={`/seasons/${season.id}/auction/fall`}>
                    <span className="topps-burst">
                      LIVE
                      <br />
                      NOW
                    </span>
                    🔨 Go to fall auction →
                  </Link>
                </div>

                <div className="topps-budget-row">
                  <span className="topps-stamp">${season.fall_budget_per_user} fall budget</span>
                  <span className="topps-stamp">
                    ${season.spring_budget_per_user} spring budget
                  </span>
                </div>

                <div className="topps-record-box">
                  <div className="topps-record-title">Draft Activity &mdash; Teams &amp; Spend</div>
                  <div className="topps-table-scroll">
                    <table className="topps-record">
                      <thead>
                        <tr>
                          <th>Player</th>
                          <th className="topps-num">Teams drafted</th>
                          <th className="topps-num">$ Spent</th>
                        </tr>
                      </thead>
                      <tbody>
                        {rows.map(({ user, spent, teamsDrafted }) => (
                          <tr key={user.id}>
                            <td>
                              <span className="topps-who">
                                <span className="topps-headshot">
                                  <Avatar
                                    name={user.display_name}
                                    src={user.avatar_data_url}
                                    size={22}
                                  />
                                </span>
                                {user.display_name}
                              </span>
                            </td>
                            <td className="topps-num">{teamsDrafted}</td>
                            <td className="topps-num">${spent}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
                <p className="topps-note">
                  This is a draft-activity snapshot, not performance-based standings &mdash;
                  real-world scoring for the active season isn&rsquo;t wired up yet. Once it is,
                  this table will rank by points instead.
                </p>

                {scoringSummary.owners.length > 0 && (
                  <div className="topps-highlights">
                    <h3>Fall Scoring Summary</h3>
                    <ul>
                      <li>
                        {scoringSummary.leagues
                          .map((lg) => `${lg} ${scoringSummary.season_label_by_league[lg] ?? "—"}`)
                          .join(" · ")}
                      </li>
                      <li>
                        EPL and URC are fully drafted, so those two columns are a complete
                        standings preview
                      </li>
                      <li>
                        Every other column only reflects whichever teams have actually been
                        drafted so far, not the full league
                      </li>
                      <li>
                        Scored from each league&rsquo;s current real-world table, refreshed by
                        hand from time to time rather than auto-updating live
                      </li>
                    </ul>
                    <div className="topps-table-scroll">
                      <table className="topps-record">
                        <thead>
                          <tr>
                            <th>Player</th>
                            {scoringSummary.leagues.map((lg) => (
                              <th className="topps-num" key={lg}>
                                {lg}
                              </th>
                            ))}
                            <th className="topps-num">Total</th>
                          </tr>
                        </thead>
                        <tbody>
                          {scoringSummary.owners.map((o) => (
                            <tr key={o.user_id}>
                              <td>
                                <span className="topps-who">
                                  <span className="topps-headshot">
                                    <Avatar
                                      name={o.display_name}
                                      src={users.find((u) => u.id === o.user_id)?.avatar_data_url}
                                      size={22}
                                    />
                                  </span>
                                  {o.display_name}
                                </span>
                              </td>
                              {scoringSummary.leagues.map((lg) => (
                                <td className="topps-num" key={lg}>
                                  {o.by_league[lg]?.toFixed(0) ?? 0}
                                </td>
                              ))}
                              <td className="topps-num">
                                <strong>{o.total.toFixed(0)}</strong>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}

                <div className="topps-links">
                  <h3>Set Checklist</h3>
                  <ol>
                    <li data-n="1">
                      <Link to={`/seasons/${season.id}/roster`}>View full roster →</Link>
                    </li>
                    <li data-n="2">
                      <Link to={`/seasons/${season.id}/auction/spring`}>
                        Go to spring auction →
                      </Link>
                    </li>
                  </ol>
                </div>
              </div>
            ))
          )}

          {/* ---- your league + explore, on the card back ---- */}
          <div className="topps-back">
            <h2>Your League</h2>
            <div className="topps-roster-strip">
              {users.map((u) => (
                <div className="topps-roster-card" key={u.id}>
                  <span className="topps-headshot">
                    <Avatar name={u.display_name} src={u.avatar_data_url} size={42} />
                  </span>
                  <span className="topps-name">{u.display_name}</span>
                  {u.is_commissioner && <span className="topps-commish-pin">Commish</span>}
                </div>
              ))}
            </div>
            <p className="topps-empty-season" style={{ margin: "14px 0 0" }}>
              <Link to="/players">View player profiles →</Link>
            </p>

            <div className="topps-links" style={{ marginTop: 20 }}>
              <h3>Explore</h3>
              <ol>
                <li data-n="1">
                  <Link to="/rules">Scoring rules →</Link>
                </li>
                <li data-n="2">
                  <Link to="/crib-sheet">Your crib sheet →</Link>
                </li>
                <li data-n="3">
                  <Link to="/example-scores">Example scores →</Link>
                </li>
                <li data-n="4">
                  <Link to="/seasons">All seasons →</Link>
                </li>
              </ol>
            </div>
          </div>

          <div className="topps-fineprint">
            <span>Card 1 of 1 · MegaFantasy Set</span>
            <span>Printed on the server · © 2026 MegaFantasy League</span>
          </div>
        </div>
      </div>
    </div>
  );
}
