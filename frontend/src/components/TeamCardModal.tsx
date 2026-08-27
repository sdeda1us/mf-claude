import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { api, type TeamHistory as TeamHistoryData } from "../lib/api";
import { SeasonChart, TeamMap } from "./TeamHistoryShared";

// Everywhere in the app EXCEPT the Team History page itself, clicking a
// TeamLink pops this "baseball card" up instead of navigating away — same
// bio/map/prognosis/chart content as the full page, just in a card you can
// glance at and dismiss without losing your place. Mounted once near the
// app root (see App.tsx) so any TeamLink, however deep, can trigger it via
// useTeamCardModal() without threading state through every page.
type Selection = { league: string; teamId: number };

const TeamCardModalContext = createContext<((league: string, teamId: number) => void) | null>(null);

export function useTeamCardModal(): (league: string, teamId: number) => void {
  const open = useContext(TeamCardModalContext);
  if (!open) {
    throw new Error("useTeamCardModal must be used within a TeamCardModalProvider");
  }
  return open;
}

export function TeamCardModalProvider({ children }: { children: ReactNode }) {
  const [selection, setSelection] = useState<Selection | null>(null);
  const [history, setHistory] = useState<TeamHistoryData | null>(null);

  const close = () => setSelection(null);
  const open = (league: string, teamId: number) => setSelection({ league, teamId });

  useEffect(() => {
    if (!selection) return;
    setHistory(null);
    api.get<TeamHistoryData>(`/teams/${selection.teamId}/history`).then(setHistory);
  }, [selection]);

  useEffect(() => {
    if (!selection) return;
    function onKeyDown(e: KeyboardEvent) {
      if (e.key === "Escape") close();
    }
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [selection]);

  return (
    <TeamCardModalContext.Provider value={open}>
      {children}
      {selection && (
        <div className="modal-backdrop" onClick={close}>
          <div className="modal-card rules-card team-card" onClick={(e) => e.stopPropagation()}>
            <div className="ribbon">{selection.league}</div>
            <button type="button" className="modal-close" onClick={close} aria-label="Close">
              ×
            </button>
            {!history ? (
              <p className="queue-empty team-card-loading">Loading…</p>
            ) : (
              <>
                <div className="nameplate team-card-nameplate">{history.name}</div>
                {history.latitude != null && history.longitude != null && (
                  <div className="team-card-photo">
                    <TeamMap name={history.name} latitude={history.latitude} longitude={history.longitude} />
                  </div>
                )}
                <div className="team-card-body">
                  {history.bio ? (
                    <p className="team-card-bio">{history.bio}</p>
                  ) : (
                    <p className="queue-empty">No biography written up for this team yet.</p>
                  )}
                  {history.prognosis && (
                    <>
                      <div className="team-card-section-label">Scouting report</div>
                      <p className="team-card-prognosis">{history.prognosis}</p>
                    </>
                  )}
                  {history.seasons.length > 0 && (
                    <>
                      <div className="team-card-section-label">Fantasy points by season</div>
                      <SeasonChart seasons={history.seasons} />
                    </>
                  )}
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </TeamCardModalContext.Provider>
  );
}
