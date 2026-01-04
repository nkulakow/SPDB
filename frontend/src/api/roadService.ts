import type { Dayjs } from "dayjs"
import type { PlannedRoute } from "../types"
import fetchAPI from "./fetchAPI"

const TIME_FORMAT = 'YYYY-MM-DDTHH:mm:ss'

export function planRoute(
    startLocation: string,
    endLocations: string[],
    timeStart: Dayjs,
    timeEnd: Dayjs
): Promise<PlannedRoute> {
    return fetchAPI("POST", "/planner/plan", {
        startLocation: startLocation,
        endLocations: endLocations,
        timeStart: timeStart.format(TIME_FORMAT),
        timeEnd: timeEnd.format(TIME_FORMAT),
    })
}
