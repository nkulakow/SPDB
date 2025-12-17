import heapq
from networkx import MultiGraph


def dijkstra_shortest_path(g: MultiGraph, start: int, end: int):
    priority_queue = [(0, [start])] # (distsance, path) path is from begin node to current node inclusively
    visited = set()
    current_distance: int
    current_path: list[int]

    while priority_queue:
        current_distance, current_path = heapq.heappop(priority_queue)

        current_node = current_path[-1]

        if current_node == end:
            break

        if current_node in visited:
            continue

        visited.add(current_node)

        for _, neighbor, _, edge_data in g.edges(current_node, data=True, keys=True):
            distance = current_distance + edge_data.get("weight")
            heapq.heappush(priority_queue, (distance, current_path + [neighbor]))

    return current_distance, current_path