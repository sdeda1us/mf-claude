// Empty string means "same origin, relative paths" — correct for the combined
// production deploy where the backend serves the built frontend. Local dev
// (frontend/.env) sets VITE_API_BASE_URL explicitly since the Vite dev server
// runs on a different port than the API.
export const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "";
export const WS_BASE = API_BASE
  ? API_BASE.replace(/^http/, "ws")
  : `${window.location.protocol === "https:" ? "wss" : "ws"}://${window.location.host}`;

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${API_BASE}/api${path}`, {
    ...options,
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = body.detail ?? detail;
    } catch {
      // ignore
    }
    throw new ApiError(detail, res.status);
  }

  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

export const api = {
  get: <T>(path: string) => request<T>(path),
  post: <T>(path: string, body?: unknown) =>
    request<T>(path, { method: "POST", body: body ? JSON.stringify(body) : undefined }),
  put: <T>(path: string, body?: unknown) =>
    request<T>(path, { method: "PUT", body: body ? JSON.stringify(body) : undefined }),
  del: <T>(path: string) => request<T>(path, { method: "DELETE" }),
};

export interface User {
  id: number;
  email: string;
  display_name: string;
  is_commissioner: boolean;
  avatar_data_url: string | null;
}

export interface Season {
  id: number;
  name: string;
  fall_budget_per_user: number;
  spring_budget_per_user: number;
  status: "setup" | "active" | "complete";
}

export interface Team {
  id: number;
  league: string;
  sport: string;
  name: string;
  default_value: number | null;
}

export interface Bid {
  id: number;
  user_id: number;
  amount: number;
  created_at: string;
}

export interface ReserveBid {
  amount: number;
  active: boolean;
}

export interface AuctionItem {
  id: number;
  auction_id: number;
  team: Team;
  order: number;
  status: "pending" | "active" | "sold";
  winning_user_id: number | null;
  winning_bid: number | null;
  bids: Bid[];
  bid_deadline: string | null;
  passed_user_ids: number[];
  // Private — only ever the viewer's own reserve, never another user's.
  my_reserve: ReserveBid | null;
}

export interface Auction {
  id: number;
  season_id: number;
  session: "fall" | "spring";
  status: "pending" | "live" | "complete";
  nomination_order: number[];
  turn_started_at: string;
  is_paused: boolean;
}

export interface RosterStatus {
  budget_remaining: number;
  spots_filled: number;
  spots_remaining: number;
  max_bid: number;
}

export interface AuctionState {
  auction: Auction;
  active_item: AuctionItem | null;
  remaining_budget_by_user: Record<string, number>;
  current_turn_user_id: number | null;
  roster_status_by_user: Record<string, RosterStatus>;
}

export interface RosterEntry {
  id: number;
  user_id: number;
  team: Team;
  price_paid: number;
  source: "auction" | "commissioner_correction";
}

export interface ScoringRuleLine {
  label: string;
  points: number;
}

export interface LeagueRules {
  roster_limits: Record<string, number>;
  scoring_rules: Record<string, ScoringRuleLine[]>;
  league_session: Record<string, "fall" | "spring">;
  minor_conference_teams: Record<string, string[]>;
}

export interface ScoreBreakdownItem {
  label: string;
  points: number;
}

export interface ExampleScoreRow {
  team_id: number;
  team_name: string;
  league: string;
  season_label: string;
  points: number;
  breakdown: ScoreBreakdownItem[];
}

export interface QueueEntry {
  id: number;
  user_id: number;
  team: Team;
  order: number;
}

export interface CribSheetEntry {
  id: number;
  team_id: number;
  value: number;
}
