import networkx as nx
from dijkstra import dijkstra_shortest_path, calc_edge_travel_time
from datetime import datetime, time, timedelta
from velocity_modifier import VelocityModifier
import pytest


def test_small_graph():
    g = nx.MultiGraph()
    g.add_edge(1, 2, key=0, weight=3)
    g.add_edge(1, 2, key=1, weight=4)
    g.add_edge(2, 3, weight=2)
    g.add_edge(1, 3, weight=10)
    dist, path = dijkstra_shortest_path(g, 1, 3)
    assert dist == 5
    assert path == [1, 2, 3]


def test_bigger_graph():
    g = nx.MultiGraph()

    g.add_edge(1, 2, key=0, weight=7)
    g.add_edge(1, 2, key=1, weight=3)

    g.add_edge(2, 3, weight=2)
    g.add_edge(3, 4, weight=4)

    g.add_edge(1, 4, weight=15)
    g.add_edge(2, 4, weight=10)

    g.add_edge(1, 5, weight=1)
    g.add_edge(5, 4, weight=20)

    dist, path = dijkstra_shortest_path(g, 1, 4)

    assert dist == 9
    assert path == [1, 2, 3, 4]


@pytest.fixture
def simple_velocity_modifier():
    vm_data = [
        (datetime.strptime("00:00", "%H:%M").time(), 1),
        (datetime.strptime("06:00", "%H:%M").time(), 0.5),
        (datetime.strptime("18:00", "%H:%M").time(), 1.5)
    ]
    return VelocityModifier(vm_data)


@pytest.fixture
def simple_edge_data():
    return {
        "base_v_kmph": 50,
        "length": 200
    }


@pytest.mark.parametrize(
    "start_time, expected_duration",
    [
        (time(0, 0), timedelta(hours=4)),
        (time(0, 25), timedelta(hours=4)),
        (time(4, 0), timedelta(hours=6)),
        (time(5, 32), timedelta(hours=7, minutes=32))
    ]
)
def test_calc_edge_travel_time(start_time: time, expected_duration: timedelta, simple_velocity_modifier, simple_edge_data):
    vm = simple_velocity_modifier
    edge_data = simple_edge_data
    duration, _ = calc_edge_travel_time(edge_data, vm, start_time)

    assert duration == expected_duration