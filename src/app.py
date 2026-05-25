import os
import redis
from flask import Flask, jsonify

app = Flask(__name__)

# Connect to Redis using environment variable or default to localhost
redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = int(os.environ.get('REDIS_PORT', 6379))

# Attempt to connect, but don't crash on startup if it fails (for liveness probes)
r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

@app.route('/')
def index():
    try:
        # Increment a counter in Redis
        count = r.incr('visitor_count')
        return jsonify({
            "message": "Hello from DevOps Challenge!",
            "visitor_count": count
        })
    except redis.exceptions.ConnectionError as e:
        return jsonify({"error": f"Redis connection failed: {str(e)}"}), 500

# Liveness Probe - check if app is running (doesn't need DB)
@app.route('/healthz')
def healthz():
    return jsonify({"status": "ok"}), 200

# Readiness Probe - check if we can connect to the DB
@app.route('/readyz')
def readyz():
    try:
        r.ping()
        return jsonify({"status": "ready"}), 200
    except redis.exceptions.ConnectionError:
        return jsonify({"status": "not ready", "reason": "redis connection failed"}), 503

if __name__ == '__main__':
    # Run the application
    app.run(host='0.0.0.0', port=5000)
