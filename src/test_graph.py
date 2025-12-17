import networkx as nx


def main() -> None:
    nodes_with_attrs = [
        (1, {"color": "red"}),
        (2, {"color": "blue"}),
        ("some test node", {"color": "green", "weight": 5})
    ]
    g = nx.Graph()
    g.add_nodes_from(nodes_with_attrs)
    print(g.nodes[1])


if __name__ == "__main__":
    main()