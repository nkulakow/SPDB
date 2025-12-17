import networkx as nx
from dijkstra import dijkstra_shortest_path


def main() -> None:
    g = nx.MultiGraph()
    g.add_edge(1, 2, key=0, weight=3)
    g.add_edge(1, 2, key=1, weight=4)
    g.add_edge(2, 3, weight=2)
    g.add_edge(1, 3, weight=10)
    print(dijkstra_shortest_path(g, 1, 3))


if __name__ == "__main__":
    main()