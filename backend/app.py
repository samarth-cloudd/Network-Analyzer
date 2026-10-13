from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import re
import socket
import time
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
CORS(app)

executor = ThreadPoolExecutor(max_workers=4)


def ping_test(target):
    try:
        start = time.monotonic()
        result = subprocess.run(
            ["ping", "-c", "4", "-W", "1", target],
            capture_output=True,
            text=True,
            timeout=6
        )
        output = result.stdout

        times = re.findall(r"time[=<]([\d.]+)", output)
        latencies = [float(t) for t in times]

        loss_match = re.search(r"(\d+(?:\.\d+)?)% packet loss", output)
        packet_loss = float(loss_match.group(1)) if loss_match else 100.0

        average = sum(latencies) / len(latencies) if latencies else 0.0

        differences = [
            abs(latencies[i] - latencies[i - 1])
            for i in range(1, len(latencies))
        ]
        jitter = sum(differences) / len(differences) if differences else 0.0

        return {
            "packets_sent": 4,
            "packets_received": len(latencies),
            "packet_loss": packet_loss,
            "average_latency": round(average, 2),
            "jitter": round(jitter, 2)
        }

    except (subprocess.TimeoutExpired, OSError):
        return {
            "packets_sent": 4,
            "packets_received": 0,
            "packet_loss": 100.0,
            "average_latency": 0,
            "jitter": 0
        }


def dns_test(target):
    try:
        start = time.monotonic()
        ip = socket.gethostbyname(target)
        dns_time = (time.monotonic() - start) * 1000
        return {"ip": ip, "dns_response": round(dns_time, 2)}
    except (socket.gaierror, OSError):
        return {"ip": "DNS resolution failed", "dns_response": 0}


def traceroute_test(target):
    try:
        result = subprocess.run(
            ["traceroute", "-n", "-m", "8", "-q", "1", "-w", "1", target],
            capture_output=True,
            text=True,
            timeout=10
        )

        hops = 0
        dropouts = 0

        for line in result.stdout.splitlines():
            match = re.match(r"\s*(\d+)\s+", line)
            if match:
                hops += 1
                if "*" in line and not re.search(r"\d+\.\d+\.\d+\.\d+", line):
                    dropouts += 1

        return {"route_hops": hops, "route_dropouts": dropouts}

    except (subprocess.TimeoutExpired, OSError):
        return {"route_hops": 0, "route_dropouts": 0}

@app.route("/api/network")
def network():
    target = request.args.get("target", "google.com").strip()

    if not target or len(target) > 253:
        return jsonify({"error": "Invalid target"}), 400

    try:
        socket.inet_aton(target)
    except OSError:
        if not re.fullmatch(
            r"(?=.{1,253}$)(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)(?:\.(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?))*",
            target
        ):
            return jsonify({"error": "Invalid target"}), 400

    # Return ping and DNS metrics without waiting for traceroute.
    dns_result = {"ip": "DNS resolution failed", "dns_response": 0}
    ping_result = {
        "packets_sent": 4,
        "packets_received": 0,
        "packet_loss": 100.0,
        "average_latency": 0,
        "jitter": 0
    }

    dns_future = executor.submit(dns_test, target)
    ping_future = executor.submit(ping_test, target)

    try:
        dns_result = dns_future.result(timeout=3)
    except TimeoutError:
        pass

    try:
        ping_result = ping_future.result(timeout=7)
    except TimeoutError:
        pass

    return jsonify({
        "target": target,
        **dns_result,
        **ping_result,
        "route_hops": 0,
        "route_dropouts": 0
    })



    def add_route():
        return traceroute_test(target)

    route_future = executor.submit(add_route)
    try:
        result.update(route_future.result(timeout=2))
    except TimeoutError:
        route_future.cancel()

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=False)

