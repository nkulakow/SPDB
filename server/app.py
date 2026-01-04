from datetime import datetime, time
from flask import Flask, jsonify, request
from flask_cors import CORS
from src.routing_service import find_shortest_paths
from src.extensions import GLOBAL_GRAPH

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
    result = find_shortest_paths(
        start_location,
        end_locations,
        datetime.combine(datetime.today(), time(hour=start_time)),
        datetime.combine(datetime.today(), time(hour=end_time)),
    )
    # print("\n\n\n", result, "\n\n\n")
    print(GLOBAL_GRAPH)
    return jsonify(
        {
            "start": {"name": "Point A", "latitude": 52.25, "longitude": 21.02},
            "routes": [
                {
                    "destination": {"name": "Point B", "latitude": 52.31, "longitude": 21.07},
                    "plannedStartTime": "11:15",
                    "nodes": [{"latitude": 52.26, "longitude": 21.03}, {"latitude": 52.28, "longitude": 21.04}],
                },
                {
                    "destination": {"name": "Point C", "latitude": 52.22, "longitude": 20.99},
                    "plannedStartTime": "11:45",
                    "nodes": [{"latitude": 52.22, "longitude": 21.02}],
                },
            ],
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
