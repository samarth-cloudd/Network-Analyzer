import socket
import time

domain = "google.com"

start = time.time()

ip = socket.gethostbyname(domain)

end = time.time()

dns_time = (end - start) * 1000

print("DNS Report")
print("----------------")
print(f"Domain:          {domain}")
print(f"Resolved IP:     {ip}")
print(f"DNS response:    {dns_time:.2f} ms")
