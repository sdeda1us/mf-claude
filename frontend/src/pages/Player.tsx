import { Link, useParams } from "react-router-dom";
import PlayerRosterPanel from "../components/PlayerRosterPanel";

export default function Player() {
  const { seasonId, userId } = useParams();

  if (!seasonId || !userId) return null;

  return (
    <div className="page">
      <p>
        <Link to={`/seasons/${seasonId}/roster`}>← Back to rosters</Link>
      </p>
      <PlayerRosterPanel seasonId={seasonId} userId={userId} />
    </div>
  );
}
