import time
from flask import Flask, jsonify, request
from flask_cors import CORS
from src.dijkstra import dijkstra_shortest_path_variable_time

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])


@app.route("/")
def index():
    return jsonify({"message": "Hello, world!"})


@app.route("/planner/plan", methods=["POST"])
def plan_route():
    data = request.get_json()  # parses JSON into a Python dict
    print(data)
    # return jsonify({"error": "Bad node: aa"}), 400 # Example error response
    time.sleep(0.1)  # Simulate processing delay
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
