from datetime import datetime, timedelta
from dataclasses import dataclass
from networkx import MultiDiGraph
import osmnx as ox

from src.extensions import GLOBAL_GRAPH
from src.dijkstra import dijkstra_shortest_path_variable_time
from src.velocity_modifier import VelocityModifier


@dataclass(slots=True)
class ShortestPathInfo:
    destination: str
    start_time: datetime
    travel_time: timedelta
    path: list[int]


def find_nearest_node(g: MultiDiGraph, location: str) -> int:
    lat, lon = ox.geocode(location)
    return ox.nearest_nodes(g, lon, lat)


def get_start_times(start_time: datetime, end_time: datetime) -> list[datetime]:
    return [start_time + i * timedelta(minutes=15) for i in range(int((end_time - start_time).total_seconds() // 900) + 1)]


def create_shortest_path_info(
    end_location: str,
    start_time: datetime,
    travel_time: timedelta,
    path: list[int]
) -> ShortestPathInfo:
    path_data = [{"latitude": GLOBAL_GRAPH.nodes[node]["y"], "longitude": GLOBAL_GRAPH.nodes[node]["x"]} for node in path]
    return ShortestPathInfo(end_location, start_time, travel_time, path_data)


def find_shortest_paths(
    start_location: str,
    end_locations: list[str],
    start_time: datetime,
    end_time: datetime
) -> dict[str, ShortestPathInfo]:
    vm = VelocityModifier([
        (datetime.strptime("00:00", "%H:%M").time(), 1.0),
        (datetime.strptime("06:00", "%H:%M").time(), 1.2),
        (datetime.strptime("18:00", "%H:%M").time(), 0.8),
    ])
    start_node = find_nearest_node(GLOBAL_GRAPH, start_location)
    end_nodes = [find_nearest_node(GLOBAL_GRAPH, loc) for loc in end_locations]
    start_times = get_start_times(start_time, end_time)
    results = {}
    for end_node, end_location in zip(end_nodes, end_locations):
        best_time = None
        best_path = None
        best_start_time = None
        for st in start_times:
            travel_time, path = dijkstra_shortest_path_variable_time(
                g=GLOBAL_GRAPH,
                start=start_node,
                end=end_node,
                velocity_modifier=vm,
                start_time=st,
                best_time=best_time
            )
            if len(path) > 0 and (best_time is None or travel_time < best_time):
                best_time = travel_time
                best_path = path
                best_start_time = st

        results[end_location] = create_shortest_path_info(
            end_location=end_location,
            start_time=best_start_time,
            travel_time=best_time,
            path=best_path
        )
    return results

