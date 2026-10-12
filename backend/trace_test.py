import subprocess
import sys
import re

# Get target from command line
if len(sys.argv) > 1:
    target = sys.argv[1]
else:
    target = "google.com"

# Run traceroute
result = subprocess.run(
    ["traceroute", "-m", "15", target],
    capture_output=True,
    text=True
)

output = result.stdout

print("\nTraceroute Report")
print("----------------")

for line in output.splitlines():
    # Find lines beginning with a hop number
    match = re.match(r"\s*(\d+)\s+(.*)", line)

    if match:
        hop = match.group(1)
        details = match.group(2)

        # Extract IP address if available
        ip_match = re.search(r"(\d+\.\d+\.\d+\.\d+)", details)

        # Extract RTT values
        times = re.findall(r"([\d.]+)\s*ms", details)

        if ip_match:
            ip = ip_match.group(1)
        else:
            ip = "Unknown"

        if times:
            avg_time = sum(float(t) for t in times) / len(times)
            print(f"Hop {hop:>2}: {ip:<16} {avg_time:.2f} ms")
        else:
            print(f"Hop {hop:>2}: {ip:<16} No response")

