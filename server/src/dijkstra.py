import heapq
from networkx import MultiGraph
from src.velocity_modifier import VelocityModifier
from datetime import datetime, timedelta


def dijkstra_shortest_path(g: MultiGraph, start: int, end: int) -> tuple[int, list[int]]:
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


def calc_edge_travel_time(edge_data: dict, velocity_modifier: VelocityModifier, start_time: datetime) -> datetime:
    """
    Calculates travel time for edge with provided edge_data, using modifications provided by velocirt_modifier.

    :return: time after crossing the edge
    """
    v_base = edge_data.get("speed_kph")

    if isinstance(v_base, str):
        v_base = int(v_base)
    elif isinstance(v_base, list):
        v_base = max(int(segment_v) for segment_v in edge_data.get("maxspeed"))
    edge_length = edge_data.get("length") / 1000
    total_distance = 0
    current_time = start_time

    while total_distance < edge_length:
        time_slot = velocity_modifier.find_time_slot(current_time)
        v = v_base * time_slot.modifier
        max_time_in_slot = velocity_modifier.get_max_time_in_slot(current_time)
        distance = v * max_time_in_slot.total_seconds() / 3600

        if total_distance + distance <= edge_length:
            current_time += max_time_in_slot
        else:
            distance = edge_length - total_distance
            hours_needed = distance / v
            current_time += timedelta(hours=hours_needed)

        total_distance += distance

    return current_time


def dijkstra_shortest_path_variable_time(
        g: MultiGraph,
        start: int,
        end: int,
        velocity_modifier: VelocityModifier,
        start_time: datetime
    ) -> tuple[datetime, list[int]]:
    """
    Dijkstra shortest path algorithm modified to calculate graph edge travel times dinamically based on information
    provided by velocity_modifier. Algorithm assumes that start and and are valid, existing nodes for graph g.
    """
    priority_queue = [(start_time, [start])] # (distsance, path) path is from begin node to current node inclusively
    visited = set()
    current_time: int
    current_path: list[int] = []
    current_node: int

    while priority_queue:
        current_time, current_path = heapq.heappop(priority_queue)

        current_node = current_path[-1]

        if current_node == end:
            break

        visited.add(current_node)

        for _, neighbor, _, edge_data in g.edges(current_node, data=True, keys=True):
            if neighbor not in visited:
                time_after_edge = calc_edge_travel_time(edge_data, velocity_modifier, current_time)
                heapq.heappush(priority_queue, (time_after_edge, current_path + [neighbor]))

    if current_node == end:
        return current_time, current_path
    return start_time, []
