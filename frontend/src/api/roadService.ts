import type { PlannedRoute } from "../types"
import fetchAPI from "./fetchAPI"

export function planRoute(
    startLocation: string,
    endLocations: string[],
    timeStart: number,
    timeEnd: number
): Promise<PlannedRoute> {
    return fetchAPI("POST", "/planner/plan", {
        startLocation: startLocation,
        endLocations: endLocations,
        timeStart: timeStart,
        timeEnd: timeEnd,
    })
}
