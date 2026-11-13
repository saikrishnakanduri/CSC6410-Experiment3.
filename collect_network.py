
import json
import socket
import psutil
import subprocess
import ipaddress
from datetime import datetime

# Run a Windows PowerShell command and return its output.
def run_powershell(command):
    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()


# Get the computer's network interfaces.
interfaces = []
addresses = psutil.net_if_addrs()
statuses = psutil.net_if_stats()

for name, address_list in addresses.items():
    interface = {
        "name": name,
        "oper-status": "up" if statuses.get(name) and statuses[name].isup else "down"
    }

    # Identify the interface type.
    lower_name = name.lower()

    if "wi-fi" in lower_name or "wireless" in lower_name:
        interface["type"] = "wifi"
    elif "loopback" in lower_name:
        interface["type"] = "loopback"
    elif "virtual" in lower_name or "vethernet" in lower_name or "ethernet 2" == lower_name:
        interface["type"] = "virtual"
    elif "ethernet" in lower_name:
        interface["type"] = "ethernet"
    else:
        interface["type"] = "other"

    if name in statuses:
        interface["mtu"] = statuses[name].mtu

    ipv4_addresses = []
    ipv6_addresses = []

    for addr in address_list:
        if addr.family == psutil.AF_LINK:
            mac = addr.address.replace("-", ":").lower()
            if len(mac.split(":")) == 6:
                interface["mac"] = mac

        elif addr.family == socket.AF_INET:
            if addr.netmask:
                network = ipaddress.IPv4Network(
                    f"{addr.address}/{addr.netmask}",
                    strict=False
                )
                ipv4_addresses.append(
                    f"{addr.address}/{network.prefixlen}"
                )

        elif addr.family == socket.AF_INET6:
            ipv6_addresses.append(addr.address)

    interface["ipv4"] = ipv4_addresses
    interface["ipv6"] = ipv6_addresses
    interfaces.append(interface)


# Read the default IPv4 gateway.
gateway = run_powershell(
    "Get-NetRoute -DestinationPrefix '0.0.0.0/0' | "
    "Sort-Object RouteMetric | "
    "Select-Object -First 1 -ExpandProperty NextHop"
)

# Read DNS server addresses.
dns_output = run_powershell(
    "Get-DnsClientServerAddress | "
    "ForEach-Object { $_.ServerAddresses } | "
    "Sort-Object -Unique"
)

dns_servers = [
    line.strip()
    for line in dns_output.splitlines()
    if line.strip()
]

# Create the observed network configuration.
host = {
    "hostname": socket.gethostname(),
    "os": "windows",
    "collected-at": datetime.now().astimezone().isoformat(),
    "dns-server": dns_servers,
    "interface": interfaces
}

if gateway:
    host["default-gateway"] = gateway

observed = {
    "student-host:host": host
}

# Save collected information in JSON format.
with open("observed.json", "w", encoding="utf-8") as file:
    json.dump(observed, file, indent=2)

print("Network information collected successfully.")
print("File created: observed.json")
print("Total interfaces:", len(interfaces))
