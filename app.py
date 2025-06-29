from flask import Flask, request, jsonify
from time import time
from typing import Dict, List
from data import mock_dataset, auxiliary_data, providers

app = Flask(__name__)

# Simple IP-based rate limiting
rate_limits: Dict[str, List[float]] = {}
RATE_LIMIT = 60  # max requests
RATE_PERIOD = 60  # per seconds

@app.before_request
def limit_requests():
    ip = request.remote_addr or 'unknown'
    now = time()
    if ip not in rate_limits:
        rate_limits[ip] = []

    # keep only timestamps within window
    rate_limits[ip] = [ts for ts in rate_limits[ip] if now - ts < RATE_PERIOD]
    rate_limits[ip].append(now)

    if len(rate_limits[ip]) > RATE_LIMIT:
        return jsonify({"error": "Rate limit exceeded"}), 429

@app.route("/charges", methods=["GET"])
def get_charges():
    search = request.args.get("search", "").lower()

    # Filter by provider name if search term provided
    if search:
        matching_provider_ids = [
            pid for pid, name in providers.items() if search in name.lower()
        ]
        filtered = [entry for entry in mock_dataset if entry["provider_id"] in matching_provider_ids]
    else:
        filtered = mock_dataset

    return jsonify({
        "data": filtered,
        "auxiliary_data": auxiliary_data
    })

@app.route("/")
def index():
    return "API is working!"

if __name__ == "__main__":
    app.run(debug=True)
