import osmnx as ox
import folium
from shapely.geometry import mapping
from pprint import pprint


def visualize_graph(graph, point: tuple[float, float], highlight_edge=None):
    """
    highlight_edge: tuple (u, v, key) of the edge to draw in a different color
    """
    nodes, edges = ox.graph_to_gdfs(graph)

    min_lon, min_lat, max_lon, max_lat = edges.total_bounds

    # Base map
    m = folium.Map(
        location=point,
        zoom_start=16,
        min_zoom=7,
        max_bounds=True,
        min_lat=min_lat - 0.01,
        max_lat=max_lat + 0.01,
        min_lon=min_lon - 0.01,
        max_lon=max_lon + 0.01,
    )

    # Draw all edges
    folium.GeoJson(edges, style_function=lambda x: {"color": "blue", "weight": 2}).add_to(m)

    # Highlight a single edge in red
    if highlight_edge:
        u, v, key = highlight_edge
        if key in graph[u][v]:
            edge_data = graph[u][v][key]
            geom = edge_data.get("geometry")
            if geom is None:
                # fallback: straight line between nodes
                coords = [(graph.nodes[u]['y'], graph.nodes[u]['x']),
                          (graph.nodes[v]['y'], graph.nodes[v]['x'])]
                folium.PolyLine(coords, color="red", weight=5).add_to(m)
            else:
                # LineString geometry
                folium.GeoJson(
                    mapping(geom),
                    style_function=lambda x: {"color": "red", "weight": 5}
                ).add_to(m)

    # Save map
    m.save("warszawa_graph.html")


def main():
    address = "Warszawa Centralna"
    point = ox.geocode(address)

    g = ox.graph_from_point(point, dist=1000, network_type="drive")
    ox.add_edge_speeds(g)

    node = list(g.nodes)[0]
    neighbor = list(g.neighbors(node))[0]

    pprint(dict(g[node][neighbor]))


if __name__ == "__main__":
    main()
