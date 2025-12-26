"""
This module exists for testing purposes during development.
"""
import osmnx as ox


address = "Warszawa Centralna"
point = ox.geocode(address)
g = ox.graph_from_point(point, dist=1000, network_type="drive")
u, v, k, data = next(iter(g.edges(keys=True, data=True)))
print(data.keys())
