from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

listings_store = []

@app.route("/")
def index():
    return jsonify({"status": "EstateScout API running"})

@app.route("/api/ingest", methods=["POST"])
def ingest():
    global listings_store
    data = request.json or {}
    listings_store = data.get("listings", [])
    return jsonify({"received": len(listings_store)})

@app.route("/api/listings")
def get_listings():
    return jsonify(listings_store)

@app.route("/api/health")
def health():
    return jsonify({"ok": True})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
