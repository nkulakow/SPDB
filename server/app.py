from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from src.service.routing_service import find_shortest_paths
from src.exceptions import LocationNotFoundError


app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])


@app.route("/")
def index():
    return jsonify({"message": "Hello, world!"})


@app.route("/planner/plan", methods=["POST"])
def plan_route():
    data = request.get_json()
    start_location = data.get("startLocation")
    end_locations = data.get("endLocations")
    start_time = data.get("timeStart")
    end_time = data.get("timeEnd")
    try:
        result = find_shortest_paths(
            start_location,
            end_locations,
            datetime.fromisoformat(start_time),
            datetime.fromisoformat(end_time),
        )
        response = {
            "start": {
                "name": start_location,
                "latitude": result[end_locations[0]].path[0]["latitude"],
                "longitude": result[end_locations[0]].path[0]["longitude"],
            },
            "routes": [
                {
                    "destination": {"name": dest, "latitude": info.path[-1]["latitude"], "longitude": info.path[-1]["longitude"]},
                    "plannedStartTime": info.start_time.strftime("%H:%M"),
                    "plannedEndTime": (info.start_time + info.travel_time).strftime("%H:%M"),
                    "nodes": info.path
                } for dest, info in result.items()],
        }
    except LocationNotFoundError:
        return jsonify({"error": f"Location '{start_location}' not found."}), 404
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
