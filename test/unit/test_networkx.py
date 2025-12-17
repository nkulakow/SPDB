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
