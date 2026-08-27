import { Link, useLocation } from "react-router-dom";
import { COVERED_TEAM_HISTORY_LEAGUES, teamHistoryHref } from "../lib/teamHistory";
import { useTeamCardModal } from "./TeamCardModal";

// Renders a team's name as a link to its team info — used everywhere a team
// name shows up in the app (auction board, crib sheet, rosters, queue,
// example scores). Falls back to plain text for leagues that don't have a
// team page yet, since there'd be nothing to show either way.
//
// On the Team History page itself this still navigates there (opening in a
// new tab) since that's the picker this link would otherwise just be
// duplicating. Everywhere else, it pops up a "baseball card" modal with the
// same info instead of navigating away and losing whatever you were doing.
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
  const location = useLocation();
  const openCard = useTeamCardModal();

  if (!COVERED_TEAM_HISTORY_LEAGUES.includes(league)) {
    return <>{name}</>;
  }

  const linkClassName = className ? `team-link ${className}` : "team-link";

  if (location.pathname === "/team-history") {
    return (
      <Link
        to={teamHistoryHref(league, teamId)}
        target="_blank"
        rel="noopener noreferrer"
        className={linkClassName}
        onClick={(e) => e.stopPropagation()}
        title={`Open ${name}'s team page in a new tab`}
      >
        {name}
      </Link>
    );
  }

  return (
    <button
      type="button"
      className={`${linkClassName} team-link-button`}
      onClick={(e) => {
        e.stopPropagation();
        openCard(league, teamId);
      }}
      title={`View ${name}'s team card`}
    >
      {name}
    </button>
  );
}
