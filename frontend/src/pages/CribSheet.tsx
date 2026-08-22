import { useEffect, useMemo, useState } from "react";
import { api, type CribSheetEntry, type LeagueRules, type Team } from "../lib/api";

export default function CribSheet() {
  const [teams, setTeams] = useState<Team[]>([]);
  const [entries, setEntries] = useState<CribSheetEntry[]>([]);
  const [rules, setRules] = useState<LeagueRules | null>(null);
  const [nameFilter, setNameFilter] = useState("");
  const [addSearch, setAddSearch] = useState("");
  const [addedTeamIds, setAddedTeamIds] = useState<Set<number>>(new Set());
  const [drafts, setDrafts] = useState<Record<number, string>>({});
  const [expandedLeagues, setExpandedLeagues] = useState<Set<string>>(new Set());
  const [showMethodology, setShowMethodology] = useState(false);
  const [sortKey, setSortKey] = useState<"name" | "value">("value");
  const [sortDir, setSortDir] = useState<"asc" | "desc">("desc");

  useEffect(() => {
    api.get<Team[]>("/teams").then(setTeams);
    api.get<CribSheetEntry[]>("/crib-sheet").then(setEntries);
    api.get<LeagueRules>("/leagues/rules").then(setRules);
  }, []);

  const valueByTeamId = useMemo(
    () => new Map(entries.map((e) => [e.team_id, e.value])),
    [entries]
  );

  const minorConferenceNames = useMemo(() => {
    const map = new Map<string, Set<string>>();
    if (rules) {
      for (const [league, names] of Object.entries(rules.minor_conference_teams)) {
        map.set(league, new Set(names));
      }
    }
    return map;
  }, [rules]);

  const isHiddenByDefault = (team: Team) => minorConferenceNames.get(team.league)?.has(team.name) ?? false;
  const isVisible = (team: Team) =>
    !isHiddenByDefault(team) || valueByTeamId.has(team.id) || addedTeamIds.has(team.id);

  const hasOverride = (teamId: number) => valueByTeamId.has(teamId);

  // The value a team is actually showing right now — the user's own
  // override if they've set one, else its modeled default, else nothing
  // (spring-session teams, not priced yet).
  const effectiveValue = (team: Team) => valueByTeamId.get(team.id) ?? team.default_value ?? null;

  const toggleSort = (key: "name" | "value") => {
    if (key === sortKey) {
      setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    } else {
      setSortKey(key);
      setSortDir(key === "value" ? "desc" : "asc");
    }
  };
  const sortArrow = (key: "name" | "value") => (sortKey === key ? (sortDir === "asc" ? " ▲" : " ▼") : "");

  const draftFor = (team: Team) => {
    if (team.id in drafts) return drafts[team.id];
    const value = valueByTeamId.get(team.id);
    if (value != null) return String(value);
    return team.default_value != null ? String(team.default_value) : "";
  };

  const save = async (teamId: number, raw: string) => {
    const trimmed = raw.trim();
    const current = valueByTeamId.get(teamId);
    if (trimmed === "") {
      if (current == null) return;
      await api.del(`/crib-sheet/${teamId}`);
      setEntries((prev) => prev.filter((e) => e.team_id !== teamId));
      return;
    }
    const value = Number(trimmed);
    if (!Number.isFinite(value) || value === current) return;
    const entry = await api.put<CribSheetEntry>(`/crib-sheet/${teamId}`, { value });
    setEntries((prev) => [...prev.filter((e) => e.team_id !== teamId), entry]);
  };

  const restoreOne = async (teamId: number) => {
    if (!hasOverride(teamId)) return;
    await api.del(`/crib-sheet/${teamId}`);
    setEntries((prev) => prev.filter((e) => e.team_id !== teamId));
    setDrafts((prev) => {
      const next = { ...prev };
      delete next[teamId];
      return next;
    });
  };

  const restoreAll = async () => {
    if (entries.length === 0) return;
    if (
      !window.confirm(
        `Restore all ${entries.length} of your custom values back to their defaults? This can't be undone.`
      )
    ) {
      return;
    }
    await api.del("/crib-sheet");
    setEntries([]);
    setDrafts({});
  };

  const addTeam = (teamId: number) => {
    setAddedTeamIds((prev) => new Set(prev).add(teamId));
    setAddSearch("");
  };

  const toggleLeague = (league: string) => {
    setExpandedLeagues((prev) => {
      const next = new Set(prev);
      if (next.has(league)) next.delete(league);
      else next.add(league);
      return next;
    });
  };

  const bySession = useMemo(() => {
    const groups: Record<"fall" | "spring" | "other", Team[]> = { fall: [], spring: [], other: [] };
    const filtered = teams.filter((t) => t.name.toLowerCase().includes(nameFilter.toLowerCase()));
    for (const t of filtered) {
      if (!isVisible(t)) continue;
      const session = rules?.league_session[t.league];
      groups[session === "fall" || session === "spring" ? session : "other"].push(t);
    }
    for (const list of Object.values(groups)) {
      list.sort((a, b) => a.league.localeCompare(b.league) || a.name.localeCompare(b.name));
    }
    return groups;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [teams, nameFilter, rules, valueByTeamId, addedTeamIds]);

  const byLeagueWithinSession = (rows: Team[]) => {
    const grouped: Record<string, Team[]> = {};
    for (const t of rows) {
      (grouped[t.league] ??= []).push(t);
    }
    return grouped;
  };

  const hiddenSearchResults = useMemo(() => {
    if (addSearch.trim().length < 2) return [];
    const query = addSearch.toLowerCase();
    return teams
      .filter((t) => isHiddenByDefault(t) && !isVisible(t) && t.name.toLowerCase().includes(query))
      .slice(0, 8);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [addSearch, teams, minorConferenceNames, valueByTeamId, addedTeamIds]);

  const renderSession = (title: string, rows: Team[]) => {
    const byLeague = byLeagueWithinSession(rows);
    const leagues = Object.keys(byLeague).sort();
    return (
      <div key={title} className="crib-session">
        <h2>{title}</h2>
        {leagues.length === 0 ? (
          <p className="queue-empty">No teams match here.</p>
        ) : (
          leagues.map((league) => {
            const leagueTeams = [...byLeague[league]].sort((a, b) => {
              const cmp =
                sortKey === "value"
                  ? (effectiveValue(a) ?? -1) - (effectiveValue(b) ?? -1)
                  : a.name.localeCompare(b.name);
              return sortDir === "asc" ? cmp : -cmp;
            });
            const expanded = expandedLeagues.has(league);
            return (
              <div key={league} className="league-block">
                <button
                  type="button"
                  className="league-caret"
                  onClick={() => toggleLeague(league)}
                  aria-expanded={expanded}
                  title={expanded ? "Collapse" : "Expand"}
                >
                  <span className={expanded ? "caret-icon open" : "caret-icon"}>▸</span>
                  <span className="league-name">{league}</span>
                  <span className="crib-league-count">({leagueTeams.length})</span>
                </button>
                {expanded && (
                  <table className="sortable-table crib-sheet-table">
                    <thead>
                      <tr>
                        <th onClick={() => toggleSort("name")}>Team{sortArrow("name")}</th>
                        <th>Sport</th>
                        <th onClick={() => toggleSort("value")}>Your Value{sortArrow("value")}</th>
                        <th></th>
                      </tr>
                    </thead>
                    <tbody>
                      {leagueTeams.map((team) => {
                        const overridden = hasOverride(team.id);
                        return (
                          <tr key={team.id}>
                            <td>{team.name}</td>
                            <td>{team.sport}</td>
                            <td className="crib-value-cell">
                              <input
                                type="number"
                                className={overridden ? "crib-value-input" : "crib-value-input is-default"}
                                placeholder="—"
                                value={draftFor(team)}
                                onChange={(e) =>
                                  setDrafts((prev) => ({ ...prev, [team.id]: e.target.value }))
                                }
                                onBlur={(e) => save(team.id, e.target.value)}
                              />
                            </td>
                            <td className="crib-restore-cell">
                              <button
                                type="button"
                                className="crib-restore-one"
                                disabled={!overridden}
                                title={overridden ? "Restore this team's default value" : "Already at its default value"}
                                onClick={() => restoreOne(team.id)}
                              >
                                ↺
                              </button>
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                )}
              </div>
            );
          })
        )}
      </div>
    );
  };

  return (
    <div className="page page-wide">
      <h1>Crib Sheet</h1>
      <p>
        Your own valuation for each team, split by which auction session drafts it — a private
        reference sheet only you can see, for you to check against during a live auction. Fall-
        session teams start pre-filled with a modeled expected-value price (shown in a lighter
        shade)
        <button
          type="button"
          className="league-info-btn crib-methodology-btn"
          onClick={() => setShowMethodology(true)}
          title="How these default values are calculated"
        >
          ?
        </button>
        ; type over one to make it yours, or use the restore buttons to drop back to that
        default. Minor-conference college football/basketball teams are hidden by default; search
        below to add one. Click a league to expand it.
      </p>

      <div className="team-board-controls">
        <input
          type="text"
          placeholder="Filter by team name…"
          value={nameFilter}
          onChange={(e) => setNameFilter(e.target.value)}
        />
        <button
          type="button"
          className="btn-primary"
          disabled={entries.length === 0}
          onClick={restoreAll}
        >
          Restore all defaults
        </button>
      </div>

      <div className="crib-add-panel">
        <label>
          Add a minor-conference college team
          <input
            type="text"
            placeholder="Search NCAAF / NCAAMB / NCAAWB teams not shown above…"
            value={addSearch}
            onChange={(e) => setAddSearch(e.target.value)}
          />
        </label>
        {hiddenSearchResults.length > 0 && (
          <ul className="crib-add-results">
            {hiddenSearchResults.map((team) => (
              <li key={team.id}>
                <span>
                  {team.name} <span className="pill">{team.league}</span>
                </span>
                <button type="button" onClick={() => addTeam(team.id)}>
                  Add
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>

      {renderSession("Fall Session", bySession.fall)}
      {renderSession("Spring Session", bySession.spring)}
      {bySession.other.length > 0 && renderSession("Other", bySession.other)}

      {showMethodology && (
        <div className="modal-backdrop" onClick={() => setShowMethodology(false)}>
          <div className="modal-card rules-card" onClick={(e) => e.stopPropagation()}>
            <div className="ribbon">How Default Values Are Calculated</div>
            <button
              type="button"
              className="modal-close"
              onClick={() => setShowMethodology(false)}
              aria-label="Close"
            >
              ×
            </button>
            <p>
              Every fall-session team (NFL, NBA, NHL, EPL, URC, NCAAF, NCAAMB, NCAAWB, ATP, WTA)
              starts with a modeled expected-value price instead of a blank $0, so there's a sane
              opening reference before you've formed your own opinion.
            </p>
            <p>
              Each team's underlying strength score is built in two steps. First, the best real
              preseason signal available for that league is turned into a projected stat line — an
              expected regular-season record and playoff run, a predicted final points total, or
              similar. Second, that projected performance is run through <em>this league's own
              scoring rules</em> (see the Rules page) exactly the way a real season's results would
              score — so the number lands on the same scale as an actual finished season, not some
              separate rating scale.
            </p>
            <p>
              What feeds step one, by league:
            </p>
            <ul>
              <li><strong>NFL, NBA, NHL:</strong> Vegas preseason win totals and championship odds.</li>
              <li><strong>NCAAF:</strong> Vegas win totals and title odds, plus ESPN's full-field FPI ratings.</li>
              <li><strong>NCAAMB, NCAAWB:</strong> Bart Torvik's full-field T-Rank power ratings.</li>
              <li><strong>EPL:</strong> Opta's published predicted final league points.</li>
              <li><strong>URC:</strong> the closest available preseason rugby power ratings and odds.</li>
              <li><strong>ATP, WTA:</strong> current world rankings aggregated by country.</li>
            </ul>
            <p>
              Those scores are turned into dollars with a value-based-drafting model sized to a
              real auction (6 users, $400 each): every roster slot reserves $1 as a floor, and
              what's left of the combined budget is split <em>evenly per roster slot across
              leagues</em> — so a league with more roster spots draws a proportionally bigger
              share, but no league's total draw depends on the scale its own scoring formula
              happens to produce (a tennis country's score aggregating many players' results
              can't out-earn an NFL team's simpler score just because the raw numbers are bigger).
            </p>
            <p>
              Within a league, its share is divided by relative score: the worst team still
              needed to fill everyone's roster spots in that league sits at the $1 floor, every
              team ranked above it gets a share proportional to how far above that it scores
              (rounded to the nearest whole dollar), and anything ranked below that cutoff — not
              projected to be worth a roster spot to anyone — prices at $0 rather than some
              token amount.
            </p>
            <p>
              It's a proxy model, not a forecast — a reasonable starting point, not a prediction of
              what a team will actually score. Type over any value to make it yours; your own
              number always takes precedence and is only ever visible to you.
            </p>
            <p>
              Spring-session leagues (MLB, PGA, LPGA, F1, WNBA, MLS, NWSL, TDF, IPL) aren't priced
              yet — those stay blank until the same pass is done there.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
