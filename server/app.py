from flask import Flask, jsonify
from src.dijkstra import dijkstra_shortest_path_variable_time

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"message": "Hello, world!"})

if __name__ == "__main__":
    app.run(debug=True)
