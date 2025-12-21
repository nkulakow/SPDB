import heapq
from networkx import MultiGraph
from velocity_modifier import VelocityModifier
from datetime import time, datetime, timedelta


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


def calc_edge_travel_time(edge_data: dict, velocity_modifier: VelocityModifier, start_time: time) -> timedelta:
    v_base = edge_data.get("base_v_kmph")
    edge_length = edge_data.get("length")
    total_distance = 0
    current_time = start_time

    while total_distance < edge_length:
        time_slot = velocity_modifier.find_time_slot(current_time)
        v = v_base * time_slot.modifier
        distance = v * (velocity_modifier.get_max_time_in_slot(current_time).total_seconds() / 3600)

        if total_distance + distance <= edge_length:
            current_time = time_slot.end
        else:
            distance = edge_length - total_distance
            time_needed = distance / v
            current_time = (datetime.combine(datetime.today(), current_time) + timedelta(hours=time_needed)).time()

        total_distance += distance

    return datetime.combine(datetime.today(), current_time) - datetime.combine(datetime.today(), start_time)


def dijkstra_shortest_path_variable_time(
        g: MultiGraph,
        start: int,
        end: int,
        velocity_modifier: VelocityModifier,
        start_time: time
    ) -> tuple[int, list[int]]:
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

VELOCITY_MODIFIER = [
    (datetime.strptime("00:00", "%H:%M").time(), 1.0),
    (datetime.strptime("02:00", "%H:%M").time(), 1.2),
    (datetime.strptime("04:00", "%H:%M").time(), 0.8),
    (datetime.strptime("06:00", "%H:%M").time(), 1.5),
    (datetime.strptime("08:00", "%H:%M").time(), 0.5),
    (datetime.strptime("10:00", "%H:%M").time(), 1.0),
    (datetime.strptime("12:00", "%H:%M").time(), 1.3),
    (datetime.strptime("14:00", "%H:%M").time(), 1.0),
    (datetime.strptime("16:00", "%H:%M").time(), 0.9),
    (datetime.strptime("18:00", "%H:%M").time(), 1.1),
    (datetime.strptime("20:00", "%H:%M").time(), 1.0),
    (datetime.strptime("22:00", "%H:%M").time(), 0.7)
]

vm = VelocityModifier(VELOCITY_MODIFIER)
edge_data = {
    "base_v_kmph": 50,
    "length": 180
}

print(calc_edge_travel_time(edge_data, vm, time(4, 50)))
