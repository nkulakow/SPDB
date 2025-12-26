import networkx as nx
import osmnx as ox
import pytest
from datetime import time, datetime, timedelta
from src.velocity_modifier import VelocityModifier
from src.dijkstra import dijkstra_shortest_path_variable_time


@pytest.fixture(scope="module")
def osmnx_graph() -> nx.MultiDiGraph:
    address = "Warszawa Centralna"
    point = ox.geocode(address)
    g = ox.graph_from_point(point, dist=1000, network_type="drive")
    return g


@pytest.fixture(scope="module")
def vm_simple() -> VelocityModifier:
    return VelocityModifier([
        (time(0, 0), 1),
        (time(6, 30), 0.8),
        (time(9, 00), 1),
        (time(15, 30), 0.6),
        (time(18, 00), 1),
        (time(20, 30), 1.2)
    ])


@pytest.mark.parametrize(
    "start, end, start_time, expected_duration, expected_path",
    [
        ("Warszawa Centralna", "Warszawa Centralna", time(), timedelta(), [32528047]),
        ("Warszawa Centralna", "Rondo Romana Dmowskiego", time(), timedelta(), [32528047]),
    ]
)
def test_dijkstra_variable_time(
    osmnx_graph,
    vm_simple,
    start: str,
    end: str,
    start_time: time,
    expected_duration: timedelta,
    expected_path: list[int]
):
    y, x = ox.geocode(start)
    start_node = ox.nearest_nodes(osmnx_graph, x, y)
    y, x = ox.geocode(end)
    end_node = ox.nearest_nodes(osmnx_graph, x, y)
    start_time = datetime.combine(datetime.today(), start_time)
    expected_arrival_time = start_time + expected_duration
    arrival_time, path = dijkstra_shortest_path_variable_time(
        osmnx_graph,
        start_node,
        end_node,
        vm_simple,
        start_time
    )

    # assert arrival_time == expected_arrival_time
    # assert path == expected_path
