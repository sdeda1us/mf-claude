import { useEffect, useState } from "react";
import { Navigate, Route, Routes, Link, NavLink, useLocation, useParams } from "react-router-dom";
import Avatar from "./components/Avatar";
import { useAuth } from "./auth/AuthContext";
import Login from "./pages/Login";
import Home from "./pages/Home";
import Seasons from "./pages/Seasons";
import Roster from "./pages/Roster";
import AuctionRoom from "./pages/Auction";
import Admin from "./pages/Admin";
import Rules from "./pages/Rules";
import ExampleScores from "./pages/ExampleScores";
import Settings from "./pages/Settings";
import Player from "./pages/Player";
import Players from "./pages/Players";
import CribSheet from "./pages/CribSheet";

function RequireAuth({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  if (loading) return <p className="page">Loading…</p>;
  if (!user) return <Navigate to="/login" replace />;
  return <>{children}</>;
}

// The auction is drafted in two separate sessions (fall/spring) — this
// bare old URL defaults to whichever comes first in the game season.
function AuctionFallRedirect() {
  const { seasonId } = useParams();
  return <Navigate to={`/seasons/${seasonId}/auction/fall`} replace />;
}

export default function App() {
  const { user, logout } = useAuth();
  const [mobileNavOpen, setMobileNavOpen] = useState(false);
  const location = useLocation();

  useEffect(() => {
    setMobileNavOpen(false);
  }, [location.pathname]);

  return (
    <>
      {user && (
        <header className="titlebar">
          <span className="pennant" aria-hidden="true" />
          <Link to="/" className="wordmark">
            <span className="mega">Mega</span>Fantasy
          </Link>
          <button
            type="button"
            className="mobile-nav-toggle"
            aria-label={mobileNavOpen ? "Close menu" : "Open menu"}
            aria-expanded={mobileNavOpen}
            onClick={() => setMobileNavOpen((v) => !v)}
          >
            <span />
            <span />
            <span />
          </button>
          <nav className={mobileNavOpen ? "titlebar-nav mobile-open" : "titlebar-nav"}>
            <NavLink to="/" end className={({ isActive }) => (isActive ? "current" : undefined)}>
              Home
            </NavLink>
            <NavLink to="/seasons" className={({ isActive }) => (isActive ? "current" : undefined)}>
              Seasons
            </NavLink>
            <NavLink to="/players" className={({ isActive }) => (isActive ? "current" : undefined)}>
              Players
            </NavLink>
            <NavLink to="/rules" className={({ isActive }) => (isActive ? "current" : undefined)}>
              Rules
            </NavLink>
            <NavLink
              to="/example-scores"
              className={({ isActive }) => (isActive ? "current" : undefined)}
            >
              Example Scores
            </NavLink>
            <NavLink to="/crib-sheet" className={({ isActive }) => (isActive ? "current" : undefined)}>
              Crib Sheet
            </NavLink>
            {user.is_commissioner && (
              <NavLink to="/admin" className={({ isActive }) => (isActive ? "current" : undefined)}>
                Admin
              </NavLink>
            )}
          </nav>
          <span className="spacer" />
          <Link to="/settings" className="nav-identity">
            <Avatar name={user.display_name} src={user.avatar_data_url} size={24} />
            {user.display_name}
          </Link>
          <button onClick={logout}>Log out</button>
        </header>
      )}
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/"
          element={
            <RequireAuth>
              <Home />
            </RequireAuth>
          }
        />
        <Route
          path="/seasons"
          element={
            <RequireAuth>
              <Seasons />
            </RequireAuth>
          }
        />
        <Route
          path="/seasons/:seasonId/roster"
          element={
            <RequireAuth>
              <Roster />
            </RequireAuth>
          }
        />
        <Route
          path="/seasons/:seasonId/players/:userId"
          element={
            <RequireAuth>
              <Player />
            </RequireAuth>
          }
        />
        <Route
          path="/seasons/:seasonId/auction"
          element={
            <RequireAuth>
              <AuctionFallRedirect />
            </RequireAuth>
          }
        />
        <Route
          path="/seasons/:seasonId/auction/:session"
          element={
            <RequireAuth>
              <AuctionRoom />
            </RequireAuth>
          }
        />
        <Route
          path="/players"
          element={
            <RequireAuth>
              <Players />
            </RequireAuth>
          }
        />
        <Route
          path="/rules"
          element={
            <RequireAuth>
              <Rules />
            </RequireAuth>
          }
        />
        <Route
          path="/example-scores"
          element={
            <RequireAuth>
              <ExampleScores />
            </RequireAuth>
          }
        />
        <Route
          path="/crib-sheet"
          element={
            <RequireAuth>
              <CribSheet />
            </RequireAuth>
          }
        />
        <Route
          path="/admin"
          element={
            <RequireAuth>
              <Admin />
            </RequireAuth>
          }
        />
        <Route
          path="/settings"
          element={
            <RequireAuth>
              <Settings />
            </RequireAuth>
          }
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </>
  );
}
