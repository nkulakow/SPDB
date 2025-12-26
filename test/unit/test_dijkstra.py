import networkx as nx
from dijkstra import dijkstra_shortest_path, calc_edge_travel_time, dijkstra_shortest_path_variable_time
from datetime import datetime, time, timedelta
from velocity_modifier import VelocityModifier
import pytest


@pytest.fixture
def small_graph():
    g = nx.MultiGraph()
    g.add_edge(1, 2, key=0, weight=3)
    g.add_edge(1, 2, key=1, weight=4)
    g.add_edge(2, 3, weight=2)
    g.add_edge(1, 3, weight=10)
    return g


def test_small_graph(small_graph):
    dist, path = dijkstra_shortest_path(small_graph, 1, 3)
    assert dist == 5
    assert path == [1, 2, 3]


@pytest.fixture
def bigger_graph():
    g = nx.MultiGraph()
    g.add_edge(1, 2, key=0, weight=7)
    g.add_edge(1, 2, key=1, weight=3)

    g.add_edge(2, 3, weight=2)
    g.add_edge(3, 4, weight=4)

    g.add_edge(1, 4, weight=15)
    g.add_edge(2, 4, weight=10)

    g.add_edge(1, 5, weight=1)
    g.add_edge(5, 4, weight=20)
    return g


def test_bigger_graph(bigger_graph):
    dist, path = dijkstra_shortest_path(bigger_graph, 1, 4)

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
def test_calc_edge_travel_time(start_time: datetime, expected_duration: timedelta, simple_velocity_modifier, simple_edge_data):
    vm = simple_velocity_modifier
    edge_data = simple_edge_data
    start_dt = datetime.combine(datetime.today(), start_time)
    time_after_edge = calc_edge_travel_time(edge_data, vm, start_dt)

    assert time_after_edge == start_dt + expected_duration


@pytest.fixture
def simple_graph_with_edge_data():
    g = nx.MultiGraph()
    g.add_edge(1, 2, key=0, base_v_kmph=50, length=200)
    g.add_edge(2, 3, key=0, base_v_kmph=50, length=100)
    return g


def test_dijkstra_shortest_path_variable_time_simple_graph(simple_velocity_modifier, simple_graph_with_edge_data):
    start_time = datetime.combine(datetime.today(), time(5, 0))
    expected_arrival_time = start_time + timedelta(hours=11)
    arrival_time, path = dijkstra_shortest_path_variable_time(simple_graph_with_edge_data, 1, 3, simple_velocity_modifier, start_time)

    assert arrival_time == expected_arrival_time
    assert path == [1, 2, 3]


@pytest.fixture
def complex_graph_with_edge_data():
    g = nx.MultiGraph()
    g.add_edge(1, 2, key=0, base_v_kmph=50, length=200)
    g.add_edge(2, 3, key=0, base_v_kmph=50, length=100)
    g.add_edge(1, 3, key=0, base_v_kmph=100, length=350)
    g.add_edge(3, 4, key=0, base_v_kmph=60, length=50)
    g.add_edge(2, 4, key=0, base_v_kmph=100, length=120)
    g.add_edge(1, 5, key=0, base_v_kmph=70, length=500)
    g.add_edge(3, 5, key=0, base_v_kmph=100, length=260)
    g.add_node(6)
    return g


@pytest.mark.parametrize(
    "start, end, start_time, expected_duration, expected_path",
    [
        (1, 2, time(0, 0), timedelta(hours=4), [1, 2]),
        (1, 3, time(0, 0), timedelta(hours=3, minutes=30), [1, 3]),
        (1, 4, time(0, 0), timedelta(hours=4, minutes=20), [1, 3, 4]),
        (1, 5, time(0, 0), timedelta(hours=6, minutes=12), [1, 3, 5]),
        (1, 1, time(0, 0), timedelta(), [1]),
        (1, 6, time(0, 0), timedelta(), []),
    ]
)
def test_dijkstra_shortest_path_variable_time_complex_graph(
    start: int,
    end: int,
    start_time: time,
    expected_duration: timedelta,
    expected_path: list[int],
    complex_graph_with_edge_data,
    simple_velocity_modifier
):
    start_time = datetime.combine(datetime.today(), start_time)
    expected_arrival_time = start_time + expected_duration
    arrival_time, path = dijkstra_shortest_path_variable_time(
        complex_graph_with_edge_data,
        start,
        end,
        simple_velocity_modifier,
        start_time
    )

    assert arrival_time == expected_arrival_time
    assert path == expected_path
