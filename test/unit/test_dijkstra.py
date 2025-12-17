import networkx as nx


def test_small_graph():
    g = nx.MultiGraph()
    g.add_edge(1, 2, key=0, weight=3)
    g.add_edge(1, 2, key=1, weight=4)
    g.add_edge(2, 3, weight=2)
    g.add_edge(1, 3, weight=10)
