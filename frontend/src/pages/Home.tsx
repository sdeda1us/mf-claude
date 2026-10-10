import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Avatar from "../components/Avatar";
import ScoringSummaryTable from "../components/ScoringSummaryTable";
import TodaysGamesCard from "../components/TodaysGamesCard";
import YesterdaysResultsCard from "../components/YesterdaysResultsCard";
import {
  api,
  type LeagueRules,
  type RosterEntry,
  type ScoringSummary,
  type Season,
  type Team,
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

const HERO_GALLERY_IMAGES = [
  { src: "/images/nfl.webp", alt: "NFL running back breaking a tackle", label: "NFL" },
  { src: "/images/wnba.webp", alt: "WNBA guard driving past a defender", label: "WNBA" },
  { src: "/images/tennis.webp", alt: "Tennis player stretching for a backhand", label: "Tennis" },
  { src: "/images/rugby.webp", alt: "Rugby scrum", label: "URC" },
];

export default function Home() {
  const [mobileHeroIndex] = useState(() => Math.floor(Math.random() * HERO_GALLERY_IMAGES.length));
  const [seasons, setSeasons] = useState<Season[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [rules, setRules] = useState<LeagueRules | null>(null);
  const [teams, setTeams] = useState<Team[]>([]);
  const [snapshots, setSnapshots] = useState<SeasonSnapshot[]>([]);
  const [showAnnouncement, setShowAnnouncement] = useState(false);

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
          {HERO_GALLERY_IMAGES.map((img, i) => (
            <div
              key={img.src}
              className={
                i === mobileHeroIndex
                  ? "hero-gallery-item hero-gallery-item-mobile-pick"
                  : "hero-gallery-item"
              }
            >
              <img src={img.src} alt={img.alt} />
              <span className="pill hero-gallery-label">{img.label}</span>
            </div>
          ))}
        </div>
      </section>

      <section>
        <h2>Active Season</h2>
        {snapshots.length === 0 ? (
          <p>
            No season is currently active. <Link to="/seasons">See all seasons →</Link>
          </p>
        ) : (
          snapshots.map(({ season, rows, scoringSummary, todaysGames, yesterdaysResults }) => (
            <div key={season.id} className="rules-card">
              <div className="ribbon">{season.name}</div>
              <div className="todays-and-yesterday-row">
                <TodaysGamesCard games={todaysGames} />
                <YesterdaysResultsCard results={yesterdaysResults} />
              </div>
              <div className="hero-cta-row">
                <Link to={`/seasons/${season.id}/auction/fall`} className="fall-auction-cta">
                  🔨 Go to fall auction →
                </Link>
                <button
                  type="button"
                  className="announcement-cta"
                  onClick={() => setShowAnnouncement(true)}
                >
                  ⚠️ IMPORTNAT ANNOUNCEMENT - PLEASE READ
                </button>
              </div>
              <p className="rules-card-meta">
                <span className="pill">${season.fall_budget_per_user} fall budget</span>
                <span className="pill">${season.spring_budget_per_user} spring budget</span>
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

              {scoringSummary.owners.length > 0 && (
                <>
                  <h3 className="scoring-summary-heading">Fall Scoring Summary</h3>
                  <p className="crib-value-note">
                    {scoringSummary.leagues
                      .map((lg) => `${lg} ${scoringSummary.season_label_by_league[lg] ?? "—"}`)
                      .join(" · ")}{" "}
                    — EPL and URC are fully drafted, so those two columns are a complete
                    standings preview; every other column here only reflects whichever teams
                    have actually been drafted so far, not the full league. Scored from each
                    league's current real-world table, refreshed by hand from time to time
                    rather than auto-updating live, so treat it as "as of the last refresh," not
                    up-to-the-minute.
                  </p>
                  <ScoringSummaryTable scoringSummary={scoringSummary} users={users} />
                </>
              )}

              <p className="inline-form">
                <Link to={`/seasons/${season.id}/roster`}>View full roster →</Link>
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

      {showAnnouncement && (
        <div className="modal-backdrop" onClick={() => setShowAnnouncement(false)}>
          <div className="modal-card rules-card" onClick={(e) => e.stopPropagation()}>
            <div className="ribbon">Important Announcement</div>
            <button
              type="button"
              className="modal-close"
              onClick={() => setShowAnnouncement(false)}
              aria-label="Close"
            >
              ×
            </button>
            <p>
              Pizza Hut has been sold by Yum! Brands and acquired by LongRange Capital. As a
              result of this transaction, Pizza Hut, as defined in our Privacy Policy is now the
              controller of your personal data processed in connection with the Pizza Hut® brand
              and Hut Rewards® loyalty program. The transfer took place on September 1, 2026.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
