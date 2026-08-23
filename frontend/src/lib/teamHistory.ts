// Shared between the Team History page itself and TeamLink (used
// wherever a team name is rendered elsewhere in the app) — the single
// source of truth for which leagues actually have a team page to link
// to. Keep in sync with backend/app/team_history.py's coverage.
export const COVERED_TEAM_HISTORY_LEAGUES = ["EPL", "NFL", "NBA", "NHL", "URC"];

export function teamHistoryHref(league: string, teamId: number): string {
  return `/team-history?league=${encodeURIComponent(league)}&teamId=${teamId}`;
}
