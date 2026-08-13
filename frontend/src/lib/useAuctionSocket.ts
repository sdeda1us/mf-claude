import { useEffect, useRef, useState } from "react";
import { WS_BASE, api, type AuctionState } from "./api";

type ServerMessage =
  | { type: "state"; data: AuctionState }
  | { type: "error"; detail: string };

export function useAuctionSocket(auctionId: number | null) {
  const [state, setState] = useState<AuctionState | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [connected, setConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const retryRef = useRef(0);

  useEffect(() => {
    if (auctionId == null) return;

    let cancelled = false;
    let retryTimeout: ReturnType<typeof setTimeout>;

    const resync = async () => {
      try {
        const fresh = await api.get<AuctionState>(`/auctions/${auctionId}/state`);
        if (!cancelled) setState(fresh);
      } catch {
        // ignore; the socket state will catch up once reconnected
      }
    };

    const connect = () => {
      const ws = new WebSocket(`${WS_BASE}/api/ws/auction/${auctionId}`);
      wsRef.current = ws;

      ws.onopen = () => {
        if (cancelled) return;
        setConnected(true);
        retryRef.current = 0;
        resync();
      };

      ws.onmessage = (event) => {
        const message: ServerMessage = JSON.parse(event.data);
        if (message.type === "state") {
          setState(message.data);
          setError(null);
        } else if (message.type === "error") {
          setError(message.detail);
        }
      };

      ws.onclose = () => {
        if (cancelled) return;
        setConnected(false);
        const delay = Math.min(1000 * 2 ** retryRef.current, 10000);
        retryRef.current += 1;
        retryTimeout = setTimeout(connect, delay);
      };
    };

    connect();

    return () => {
      cancelled = true;
      clearTimeout(retryTimeout);
      wsRef.current?.close();
    };
  }, [auctionId]);

  const sendBid = (amount: number) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ type: "bid", amount }));
    }
  };

  const sendPass = () => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ type: "pass" }));
    }
  };

  return { state, error, connected, sendBid, sendPass };
}
