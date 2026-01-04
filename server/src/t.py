"""
This module exists for testing purposes during development.
"""
import os
import pickle
import osmnx as ox
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import time

# Files for caching
POLYGON_CACHE_FILE = "mazovia_buffered_polygon.pkl"
GRAPH_CACHE_FILE = "mazovia_drive.graphml"

places = [
    "Warsaw, Poland",
    "Piaseczno, Poland",
    "Pruszków, Poland",
    "Legionowo, Poland",
    "Otwock, Poland",
]

# 1️⃣ Check if buffered polygon exists
start = time.time()
if os.path.exists(POLYGON_CACHE_FILE):
    with open(POLYGON_CACHE_FILE, "rb") as f:
        polygon_ll = pickle.load(f)
    print("Loaded buffered polygon from cache.")
else:
    print("Downloading polygon fom API.")
    # Geocode all places
    gdfs = [ox.geocode_to_gdf(p) for p in places]
    gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True), crs="EPSG:4326")

    # Project to meters
    gdf_m = gdf.to_crs(epsg=3857)

    # Convex hull + buffer (3 km)
    polygon = gdf_m.unary_union.convex_hull.buffer(3000)

    # Back to lat/lon
    polygon_ll = gpd.GeoSeries([polygon], crs=3857).to_crs(4326).iloc[0]

    # Save polygon for future use
    with open(POLYGON_CACHE_FILE, "wb") as f:
        pickle.dump(polygon_ll, f)
    print("Buffered polygon saved to cache.")

# 2️⃣ Check if graph exists
if os.path.exists(GRAPH_CACHE_FILE):
    G = ox.load_graphml(GRAPH_CACHE_FILE)
    print("Loaded graph from cache.")
else:
    G = ox.graph_from_polygon(
        polygon_ll,
        network_type="drive"
    )
    ox.save_graphml(G, GRAPH_CACHE_FILE)
    print("Graph saved to cache.")

end = time.time()
print("Setup time:", end - start, "seconds")

# 3️⃣ Plot the graph
fig, ax = ox.plot_graph(
    G,
    node_size=0,
    edge_linewidth=0.7,
    bgcolor="white",
    show=False,
    close=False
)

# 4️⃣ Plot the buffered polygon
gpd.GeoSeries([polygon_ll]).plot(
    ax=ax,
    facecolor="none",
    edgecolor="red",
    linewidth=2,
    label="Buffered Convex Hull"
)

# 5️⃣ Plot the geocoded places
# Reload geocoded places only if polygon was not cached
if 'gdf' not in locals():
    gdfs = [ox.geocode_to_gdf(p) for p in places]
    gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True), crs="EPSG:4326")

gdf.plot(
    ax=ax,
    color="blue",
    markersize=50,
    label="Places"
)

# 6️⃣ Add legend and show
plt.legend()
plt.show()
