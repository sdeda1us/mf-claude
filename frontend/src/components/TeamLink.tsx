import { Link } from "react-router-dom";
import { COVERED_TEAM_HISTORY_LEAGUES, teamHistoryHref } from "../lib/teamHistory";

// Renders a team's name as a link to its Team History page, opening in a
// new tab — used everywhere a team name shows up in the app (auction
// board, crib sheet, rosters, queue, example scores). Falls back to
// plain text for leagues that don't have a team page yet, since linking
// there would just land on an empty picker with nothing selected.
export default function TeamLink({
  teamId,
  league,
  name,
  className,
}: {
  teamId: number;
  league: string;
  name: string;
  className?: string;
}) {
  if (!COVERED_TEAM_HISTORY_LEAGUES.includes(league)) {
    return <>{name}</>;
  }
  return (
    <Link
      to={teamHistoryHref(league, teamId)}
      target="_blank"
      rel="noopener noreferrer"
      className={className ? `team-link ${className}` : "team-link"}
      onClick={(e) => e.stopPropagation()}
      title={`Open ${name}'s team page in a new tab`}
    >
      {name}
    </Link>
  );
}
