import os
import socket
import time
import redis
from flask import Flask, render_template, jsonify

app = Flask(__name__)
START_TIME = time.time()
CONTAINER_ID = socket.gethostname()

r = redis.Redis(host="redis", port=6379, decode_responses=True)

def update_heartbeat():
    now = time.time()
    r.hset(f"node:{CONTAINER_ID}", mapping={
        "id": CONTAINER_ID,
        "uptime": round(now - START_TIME, 1),
        "last_seen": now
    })
    r.sadd("all_nodes", CONTAINER_ID)

@app.route("/")
def index():
    r.hincrby(f"node:{CONTAINER_ID}", "requests", 1)
    update_heartbeat()
    
    nodes = []
    now = time.time()
    for nid in sorted(r.smembers("all_nodes")):
        info = r.hgetall(f"node:{nid}")
        if info:
            is_alive = (now - float(info.get("last_seen", 0))) < 8
            nodes.append({
                "id": nid,
                "status": "HEALTHY" if is_alive else "RECOVERING",
                "uptime": info.get("uptime", "0"),
                "requests": info.get("requests", "0"),
                "is_alive": is_alive
            })

    logs = r.lrange("cluster_logs", 0, 5)
    return render_template("index.html", current_node=CONTAINER_ID, nodes=nodes, logs=logs)

@app.route("/ping")
def ping():
    r.hincrby(f"node:{CONTAINER_ID}", "requests", 1)
    update_heartbeat()
    return jsonify({"node": CONTAINER_ID})

@app.route("/health")
def health():
    update_heartbeat()
    return jsonify({"status": "healthy", "container": CONTAINER_ID}), 200

@app.route("/crash")
def crash():
    timestamp = time.strftime("%H:%M:%S")
    r.lpush("cluster_logs", f"[{timestamp}] [ERR] Node {CONTAINER_ID} exited (code 1)")
    r.hset(f"node:{CONTAINER_ID}", "last_seen", 0)
    os._exit(1)

if __name__ == "__main__":
    timestamp = time.strftime("%H:%M:%S")
    r.lpush("cluster_logs", f"[{timestamp}] [INFO] Node {CONTAINER_ID} started")
    update_heartbeat()
    app.run(host="0.0.0.0", port=5000)