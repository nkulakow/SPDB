from datetime import datetime
from dataclasses import dataclass
from networkx import MultiDiGraph

from src.dijkstra import dijkstra_shortest_path_variable_time


@dataclass(slots=True)
class ShortestPathInfo:
    path: list[int]
    arrival_time: datetime


def load_graph() -> MultiDiGraph:
    pass


def find_shortest_paths(
    start_location: str,
    end_locations: list[str],
    start_time: datetime,
    end_time: datetime
) -> dict[str, ShortestPathInfo]:
    g = load_graph()
