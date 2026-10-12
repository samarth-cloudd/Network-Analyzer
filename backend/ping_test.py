import subprocess
import re
import socket
import time
import sys

# Get target from command line
if len(sys.argv) > 1:
    target = sys.argv[1]
else:
    target = "google.com"

# ---------------- PING TEST ----------------

result = subprocess.run(
    ["ping", "-c", "4", target],
    capture_output=True,
    text=True
)

output = result.stdout

# Extract RTT values
times = re.findall(r"time[=<]([\d.]+)", output)
latencies = [float(t) for t in times]

# Packet loss
loss_match = re.search(r"(\d+(?:\.\d+)?)% packet loss", output)

if loss_match:
    packet_loss = float(loss_match.group(1))
else:
    packet_loss = 100.0

# Average latency
if latencies:
    average = sum(latencies) / len(latencies)
else:
    average = 0

# Jitter
if len(latencies) > 1:
    differences = [
        abs(latencies[i] - latencies[i - 1])
        for i in range(1, len(latencies))
    ]
    jitter = sum(differences) / len(differences)
else:
    jitter = 0

# ---------------- DNS TEST ----------------

try:
    start = time.time()

    ip = socket.gethostbyname(target)

    end = time.time()

    dns_time = (end - start) * 1000

except socket.gaierror:
    ip = "DNS resolution failed"
    dns_time = 0

# ---------------- REPORT ----------------

print("\nNetwork Report")
print("----------------")
print(f"Target:           {target}")
print(f"Resolved IP:      {ip}")
print(f"Packets sent:     4")
print(f"Packets received: {len(latencies)}")
print(f"Packet loss:      {packet_loss:.1f}%")
print(f"Average latency:  {average:.2f} ms")
print(f"Jitter:           {jitter:.2f} ms")
print(f"DNS response:     {dns_time:.2f} ms")
