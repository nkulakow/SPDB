import networkx as nx
from dijkstra import dijkstra_shortest_path


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
