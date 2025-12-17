import heapq
from networkx import MultiGraph


def dijkstra_shortest_path(g: MultiGraph, start: int, end: int):
    distances = {node: float("inf") for node in g}
    distances[start] = 0

    previous = {node: None for node in g.nodes}

    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node == end:
            break

        if current_distance > distances[current_node]:
            continue

        for _, neighbor, _, edge_data in g.edges(current_node, data=True, keys=True):
            distance = current_distance + edge_data.get("weight")

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    return previous, distances