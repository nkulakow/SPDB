from pathlib import Path
from networkx import MultiDiGraph
import os
import pickle
import osmnx as ox
from geopandas import GeoDataFrame


CITY = "mazowieckie"

ROOT_DIR = Path(__file__).parent.parent
STORAGE_DIR = ROOT_DIR / "storage"
POLYGON_CACHE_FILE = STORAGE_DIR / f"{CITY}_polygon.pkl"
GRAPH_CACHE_FILE = STORAGE_DIR / f"{CITY}_drive.graphml"


def load_graph() -> MultiDiGraph:
    polygon: GeoDataFrame
    g: MultiDiGraph

    if os.path.exists(POLYGON_CACHE_FILE):
        with open(POLYGON_CACHE_FILE, "rb") as f:
            polygon = pickle.load(f)
    else:
        polygon = ox.geocode_to_gdf(f"{CITY}, Poland").iloc[0].geometry
        with open(POLYGON_CACHE_FILE, "wb") as f:
            pickle.dump(polygon, f)

    if GRAPH_CACHE_FILE.exists():
        print("donwloading graph from cache")
        g = ox.load_graphml(GRAPH_CACHE_FILE)
    else:
        print("donwloading graph from API")
        g = ox.graph_from_polygon(
            polygon,
            network_type="drive",
            simplify=True
        )
        ox.save_graphml(g, GRAPH_CACHE_FILE)
    return g


GLOBAL_GRAPH = load_graph()
