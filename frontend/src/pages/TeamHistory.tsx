import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { api, type Team, type TeamHistory as TeamHistoryData } from "../lib/api";
import { COVERED_TEAM_HISTORY_LEAGUES } from "../lib/teamHistory";
import { SeasonChart, TeamMap } from "../components/TeamHistoryShared";

function TeamHistoryPanel({ teamId }: { teamId: number }) {
  const [history, setHistory] = useState<TeamHistoryData | null>(null);

  useEffect(() => {
    setHistory(null);
    api.get<TeamHistoryData>(`/teams/${teamId}/history`).then(setHistory);
  }, [teamId]);

  if (!history) return <p className="queue-empty">Loading…</p>;

  return (
    <div className="team-history-panel">
      <h2>{history.name}</h2>
      <div className="team-history-header">
        {history.bio ? (
          <p className="team-history-bio">{history.bio}</p>
        ) : (
          <p className="queue-empty">No biography written up for this team yet.</p>
        )}
        {history.latitude != null && history.longitude != null && (
          <TeamMap name={history.name} latitude={history.latitude} longitude={history.longitude} />
        )}
      </div>

      {history.prognosis && (
        <>
          <h3>Outlook for the upcoming season</h3>
          <p className="team-history-prognosis">{history.prognosis}</p>
        </>
      )}

      <h3>Fantasy points by season</h3>
      {history.seasons.length === 0 ? (
        <p className="queue-empty">
          No recent seasons to chart — {history.name} hasn't played in the {history.league} within
          the last several years covered so far.
        </p>
      ) : (
        <>
          <SeasonChart seasons={history.seasons} />
          {history.seasons.length < 5 && (
            <p className="team-history-note">
              Showing every season {history.name} has actually played in the {history.league}{" "}
              recently — fewer than 5 because of time spent in a lower division in between.
            </p>
          )}
        </>
      )}
    </div>
  );
}

function LeaguePicker({
  league,
  teams,
  selectedTeamId,
  onChange,
}: {
  league: string;
  teams: Team[];
  selectedTeamId: number | null;
  onChange: (teamId: number | null) => void;
}) {
  const sorted = [...teams].sort((a, b) => a.name.localeCompare(b.name));
  return (
    <div className="stacked-form team-history-picker">
      <label>
        {league}
        <select
          value={selectedTeamId ?? ""}
          onChange={(e) => onChange(e.target.value ? Number(e.target.value) : null)}
        >
          <option value="">Choose a team…</option>
          {sorted.map((t) => (
            <option key={t.id} value={t.id}>
              {t.name}
            </option>
          ))}
        </select>
      </label>
    </div>
  );
}

type Selection = { league: string; teamId: number } | null;

export default function TeamHistory() {
  const [teams, setTeams] = useState<Team[]>([]);
  const [searchParams] = useSearchParams();
  // Deep-link support (see components/TeamLink.tsx): a link elsewhere in
  // the app points here with ?league=&teamId=, which preselects that
  // league's picker on load — this only runs once, so picking a
  // different team afterwards isn't fought by a stale URL.
  const [selected, setSelected] = useState<Selection>(() => {
    const league = searchParams.get("league");
    const teamId = Number(searchParams.get("teamId"));
    if (league && COVERED_TEAM_HISTORY_LEAGUES.includes(league) && teamId) {
      return { league, teamId };
    }
    return null;
  });

  useEffect(() => {
    api.get<Team[]>("/teams").then(setTeams);
  }, []);

  return (
    <div className="page">
      <h1>Team History</h1>
      <p>
        A short biography and the last several seasons' worth of fantasy points for each team —
        currently covering EPL, NFL, NBA, NHL, URC, and the top 50 teams by expected fantasy
        points in each of NCAAF, NCAAMB, and NCAAWB, ahead of doing the same research pass for
        the other leagues.
      </p>

      <div className="team-history-picker-row">
        {COVERED_TEAM_HISTORY_LEAGUES.map((league) => (
          <LeaguePicker
            key={league}
            league={league}
            teams={teams.filter((t) => t.league === league)}
            // Only ever one team selected across every league's picker —
            // choosing a new one here (or clearing this one) replaces
            // whatever was picked in any other league's dropdown, rather
            // than piling up multiple histories on the page at once.
            selectedTeamId={selected?.league === league ? selected.teamId : null}
            onChange={(teamId) => setSelected(teamId ? { league, teamId } : null)}
          />
        ))}
      </div>

      {selected && (
        <section className="team-history-group">
          <TeamHistoryPanel teamId={selected.teamId} />
        </section>
      )}
    </div>
  );
}
