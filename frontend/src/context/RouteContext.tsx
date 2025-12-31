import { createContext, useContext, useState } from "react";
import type { PlannedRoute } from "../types";

type RouteContextType = {
  route: PlannedRoute | null;
  setRoute: (r: PlannedRoute) => void;
};

const RouteContext = createContext<RouteContextType | null>(null);

export function RouteProvider({ children }: { children: React.ReactNode }) {
  const [route, setRoute] = useState<PlannedRoute | null>(null);

  return (
    <RouteContext.Provider value={{ route, setRoute }}>
      {children}
    </RouteContext.Provider>
  );
}

export function useRoute() {
  const ctx = useContext(RouteContext);
  if (!ctx) throw new Error("useRoute must be used inside RouteProvider");
  return ctx;
}
