export type Node = {
    name: string
    latitude: number
    longitude: number
}

export type NamedNode = Node & {
    name: string
}

export type Route = {
    destination: NamedNode
    plannedStartTime: string
    nodes: Node[]
    color: string
}

export type PlannedRoute = {
    start: NamedNode
    routes: Route[]
}
