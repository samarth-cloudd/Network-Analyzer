from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import re
import socket
import time

app = Flask(__name__)
CORS(app)

def network_test(target):
    # ---------- PING ----------
    result = subprocess.run(
        ["ping", "-c", "4", target],
        capture_output=True,
        text=True
    )


    output = result.stdout

    times = re.findall(r"time[=<]([\d.]+)", output)
    latencies = [float(t) for t in times]

    loss_match = re.search(r"(\d+(?:\.\d+)?)% packet loss", output)

    packet_loss = float(loss_match.group(1)) if loss_match else 100.0

    average = (
        sum(latencies) / len(latencies)
        if latencies else 0
    )

    if len(latencies) > 1:
        differences = [
            abs(latencies[i] - latencies[i - 1])
            for i in range(1, len(latencies))
        ]
        jitter = sum(differences) / len(differences)
    else:
        jitter = 0

    # ---------- DNS ----------
    try:
        start = time.time()
        ip = socket.gethostbyname(target)
        end = time.time()

        dns_time = (end - start) * 1000

    except socket.gaierror:
        ip = "DNS resolution failed"
        dns_time = 0

    # ---------- RESULT ----------
    return {
        "target": target,
        "ip": ip,
        "packets_sent": 4,
        "packets_received": len(latencies),
        "packet_loss": packet_loss,
        "average_latency": round(average, 2),
        "jitter": round(jitter, 2),
        "dns_response": round(dns_time, 2)
    }


def traceroute_test(target):
    try:
        result = subprocess.run(
            ["traceroute", "-m", "15", "-w", "1", target],
            capture_output=True,
            text=True,
            timeout=20
        )

        output = result.stdout
        hops = 0
        dropouts = 0

        for line in output.splitlines():
            match = re.match(r"\s*(\d+)\s+", line)

            if match:
                hops += 1

                # Count a hop as a dropout if every probe timed out
                if "*" in line and not re.search(r"\d+\.\d+\.\d+\.\d+", line):
                    dropouts += 1

        return {
            "route_hops": hops,
            "route_dropouts": dropouts
        }

    except (subprocess.TimeoutExpired, OSError):
        return {
            "route_hops": 0,
            "route_dropouts": 0
        }

@app.route("/api/network")
def network():
    from flask import request

    target = request.args.get("target", "google.com").strip()

    result = network_test(target)
    result.update(traceroute_test(target))
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
