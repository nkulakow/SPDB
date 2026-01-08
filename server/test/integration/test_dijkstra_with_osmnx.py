import networkx as nx
import osmnx as ox
import pytest
from datetime import time, datetime, timedelta

from src.route_modeling.velocity_modifier import VelocityModifier
from src.route_modeling.dijkstra import dijkstra_shortest_path_variable_time


@pytest.fixture(scope="module")
def osmnx_graph() -> nx.MultiDiGraph:
    address = "Warszawa Centralna"
    point = ox.geocode(address)
    g = ox.graph_from_point(point, dist=1000, network_type="drive")
    ox.add_edge_speeds(g)
    return g


@pytest.fixture(scope="module")
def osmnx_highway_types() -> set[str]:
    return {
        "footway",
        "living_street",
        "motorway",
        "motorway_link",
        "pedestrian",
        "trunk",
        "trunk_link",
        "primary",
        "primary_link",
        "secondary",
        "secondary_link",
        "tertiary",
        "tertiary_link",
        "unclassified",
        "residential",
        "road",
        "track",
        "service"
    }


@pytest.fixture(scope="module")
def vm_simple(osmnx_highway_types) -> VelocityModifier:
    slots = [
        (time(0, 0), 1),
        (time(6, 30), 0.8),
        (time(9, 00), 1),
        (time(15, 30), 0.6),
        (time(18, 00), 1),
        (time(20, 30), 1.2)
    ]
    return VelocityModifier({road_type: slots for road_type in osmnx_highway_types})


@pytest.mark.parametrize(
    "start, end, start_time, expected_duration, expected_path",
    [
        ("Warszawa Centralna", "Warszawa Centralna", time(), timedelta(), [32528047]),
        (
            "Warszawa Centralna",
            "Rondo Romana Dmowskiego",
            time(),
            timedelta(seconds=57),
            [32528047, 32528045, 32528046, 32528048, 8170409961, 32629360, 2480951912, 3818807470, 105757851, 32572231]
        ),
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
    arrival_duration, path = dijkstra_shortest_path_variable_time(
        osmnx_graph,
        start_node,
        end_node,
        vm_simple,
        start_time,
        None
    )

    assert arrival_duration.total_seconds() == pytest.approx(expected_duration.total_seconds(), rel=0.1)
    assert path == expected_path
