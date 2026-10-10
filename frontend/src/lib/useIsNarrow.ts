import { useEffect, useState } from "react";

// True on narrow (roughly phone-width) viewports, re-evaluated live as the
// viewport crosses the breakpoint (e.g. on rotation or window resize).
export function useIsNarrow(breakpointPx: number): boolean {
  const [isNarrow, setIsNarrow] = useState(
    () => window.matchMedia(`(max-width: ${breakpointPx}px)`).matches
  );
  useEffect(() => {
    const mq = window.matchMedia(`(max-width: ${breakpointPx}px)`);
    const update = () => setIsNarrow(mq.matches);
    mq.addEventListener("change", update);
    return () => mq.removeEventListener("change", update);
  }, [breakpointPx]);
  return isNarrow;
}
