import networkx as nx
import pytest


NODES = [1, 2, "some test node"]
NODES_WITH_DATA = [
    (1, {"color": "red"}),
    (2, {"color": "blue"}),
    ("some test node", {"color": "green", "weight": 5})
]


def test_create_graph_with_hashable_elements():
    g = nx.Graph()
    g.add_nodes_from(NODES)


def test_create_graph_with_unhashable_elements_throws_typeerror():
    with pytest.raises(TypeError):
        g = nx.Graph()
        g.add_nodes_from([[1, 2], {"key": "value"}])


def test_created_graph_has_provided_nodes():
    nodes = NODES
    g = nx.Graph()
    g.add_nodes_from(nodes)
    assert list(g.nodes) == nodes


def test_created_graph_has_no_edges():
    g = nx.Graph()
    g.add_nodes_from(NODES)
    assert g.number_of_edges() == 0


def test_create_graph_with_node_data():
    g = nx.Graph()
    g.add_nodes_from(NODES_WITH_DATA)


def test_create_graph_with_node_data_has_provided_data():
    nodes_with_data = NODES_WITH_DATA
    g = nx.Graph()
    g.add_nodes_from(nodes_with_data)
    assert list(g.nodes.data()) == nodes_with_data


def test_access_patterns_node_data():
    g = nx.Graph()
    node = 1
    node_data = {"color": "red", "weight": 10, "travel_time": 5}
    node_tuple = (node, node_data)
    g.add_node(node, **node_data)
    assert list(g.nodes.data()) == [node_tuple]
    assert g.nodes[1] == node_data
    assert g.nodes[1]["color"] == "red"


def test_add_edges_between_existing_nodes_has_provided_edges():
    g = nx.Graph()
    g.add_nodes_from(NODES)
    g.add_edge(NODES[0], NODES[1])
    assert list(g.edges) == [(NODES[0], NODES[1])]


def test_add_edges_between_new_nodes_has_provided_nodes_and_edges():
    g = nx.Graph()
    g.add_edge(NODES[0], NODES[1])
    assert list(g.nodes) == [NODES[0], NODES[1]]
    assert list(g.edges) == [(NODES[0], NODES[1])]


def test_add_edges_has_provided_neighbors():
    g = nx.Graph()
    g.add_edges_from([(NODES[0], NODES[1]), (NODES[0], NODES[2])])
    assert list(g.neighbors(NODES[0])) == [NODES[1], NODES[2]]
    assert list(g.neighbors(NODES[1])) == [NODES[0]]
    assert list(g.neighbors(NODES[2])) == [NODES[0]]


def test_graph_iterator():
    g = nx.MultiGraph()
    g.add_edge(1, 2, weight=3)
    g.add_edge(2, 3, weight=2)
    g.add_edge(1, 3, weight=10)
    assert [node for node in g] == [1, 2, 3]


def test_neighbor_iterator():
    g = nx.MultiGraph()
    g.add_edge(1, 2, key=0, weight=3)
    g.add_edge(2, 3, key=1, weight=2)
    g.add_edge(1, 3, key=2, weight=10)
    assert [node for node in g[1]] == [2, 3]


def test_edge_access():
    g = nx.MultiGraph()
    g.add_edge(1, 2, key=0, weight=3)
    g.add_edge(2, 3, key=1, weight=2)
    g.add_edge(1, 3, key=2, weight=10)
    assert g.edges[1, 2, 0]["weight"] == 3
    assert g.edges[2, 3, 1]["weight"] == 2
    assert g.edges[1, 3, 2]["weight"] == 10


def test_multigraph_edge_iterator():
    g = nx.MultiGraph()
    g.add_edge(1, 2, key=0, weight=3)
    g.add_edge(1, 2, key=1, weight=4)
    g.add_edge(2, 3, key=0, weight=2)
    g.add_edge(1, 3, key=0, weight=10)
    expected_edges = sorted([
        (1, 2, 0, {"weight": 3}),
        (1, 2, 1, {"weight": 4}),
        (2, 3, 0, {"weight": 2}),
        (1, 3, 0, {"weight": 10})
    ])
    actual_edges = sorted(list(g.edges(data=True, keys=True)))
    assert actual_edges == expected_edges

