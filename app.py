from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory store — persists while server is running
store = {"listings": [], "last_updated": None}

@app.route("/")
def index():
    return jsonify({"status": "EstateScout API running", "listings": len(store["listings"])})

@app.route("/api/ingest", methods=["POST"])
def ingest():
    data = request.json or {}
    listings = data.get("listings", [])
    if listings:
        store["listings"] = listings
        from datetime import datetime
        store["last_updated"] = datetime.now().isoformat()
    return jsonify({"received": len(listings), "stored": len(store["listings"])})

@app.route("/api/listings")
def get_listings():
    return jsonify(store["listings"])

@app.route("/api/status")
def status():
    return jsonify({"listings": len(store["listings"]), "last_updated": store["last_updated"]})

@app.route("/api/health")
def health():
    return jsonify({"ok": True})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
