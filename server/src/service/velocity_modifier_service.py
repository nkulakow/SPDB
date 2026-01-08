import json
from pathlib import Path
from datetime import datetime

from src.config import TRAFFIC_DATA_DIR
from src.route_modeling.velocity_modifier import VelocityModifier


def load_traffic_data():
    traffic_data = {}

    for file_path in Path(TRAFFIC_DATA_DIR).glob("*.json"):
        key = file_path.stem

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        entries = []
        for time_str, value in data.items():
            time_obj = datetime.strptime(time_str, "%H:%M").time()
            entries.append((time_obj, float(value)))

        traffic_data[key] = entries

    return traffic_data

VELOCITY_MODIFIER = VelocityModifier(load_traffic_data())
