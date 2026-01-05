from datetime import datetime
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
    arrival_time: datetime
    path: list[int]


def find_nearest_node(g: MultiDiGraph, location: str) -> int:
    lat, lon = ox.geocode(location)
    return ox.nearest_nodes(g, lon, lat)


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
    results = {}
    for end_node, end_location in zip(end_nodes, end_locations):
        arrival_time, path = dijkstra_shortest_path_variable_time(GLOBAL_GRAPH, start_node, end_node, vm, start_time)
        path_data = [{"latitude": GLOBAL_GRAPH.nodes[node]["y"], "longitude": GLOBAL_GRAPH.nodes[node]["x"]} for node in path]
        results[end_location] = ShortestPathInfo(end_location, start_time, arrival_time, path_data)
    return results

