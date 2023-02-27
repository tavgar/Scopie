import argparse
import json
import re
import socket

parser = argparse.ArgumentParser(description='Update list of subdomains to match scope configuration')
parser.add_argument('--subs', type=str, required=True,
                    help='Path to subs.txt file')
parser.add_argument('--scope', type=str, required=True,
                    help='Path to scope.json file')
parser.add_argument('--output', type=str, required=True,
                    help='Path to output file')
parser.add_argument('--timeout', type=int, required=False,nargs='?', const=5, help='Timeout for the response')
args = parser.parse_args()

# Load the scope file
with open('scope.json') as f:
    scope = json.load(f)

# Extract the hosts from the scope file
hosts = []
for item in scope['target']['scope']['include']:
    if 'host' in item:
        host_pattern = item['host']
        host_pattern = host_pattern.replace('^.*', '').replace('$', '')  # remove regex anchors
        host_pattern = re.escape(host_pattern)  # escape special characters
        host_pattern = host_pattern.replace('\\\.', '.')  # unescape escaped dots
        hosts.append(re.compile(host_pattern))  # compile regex pattern

# Load the subdomain file
with open(args.subs) as f:
    subdomains = f.read().splitlines()

# Filter the subdomains based on the hosts in the scope file
matching_subdomains = []
for subdomain in subdomains:
    for host in hosts:
        if host.search(subdomain):
            matching_subdomains.append(subdomain)
            break
alive_subdomains = []
for host in matching_subdomains:
    # Try to resolve the host name to an IP address
    ip = socket.gethostbyname(host)
    try:
        # Try to connect to the IP address on port 80 (HTTP)
        s = socket.create_connection((ip, 80), timeout=args.timeout)
        s.close()
        alive_subdomains.append(host)
    except (socket.gaierror, socket.timeout, ConnectionRefusedError):
        pass
    try:
        # Try to connect to the IP address on port 443 (HTTPS)
        s = socket.create_connection((ip, 443), timeout=args.timeout)
        s.close()
        # If successful, print a message indicating the host responded on HTTPS
        if host not in alive_subdomains:
            alive_subdomains.append(host)
    except (socket.gaierror, socket.timeout, ConnectionRefusedError):
        pass
with open(args.output, 'a') as f:
    for subdomain in alive_subdomains:
        f.write(subdomain + '\n')
