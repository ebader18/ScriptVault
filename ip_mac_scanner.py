import os
import subprocess
import ipaddress
import re
import argparse

def ping_ip(ip):
    try:
        # Pinging with one packet, '-n 1', to see if host is up
        subprocess.check_output(["ping", "-n", "1", ip], stderr=subprocess.STDOUT, universal_newlines=True)
        return True
    except subprocess.CalledProcessError:
        return False

def get_mac_address(ip):
    try:
        arp_output = subprocess.check_output(['arp', '-a', ip], universal_newlines=True)
        # Adjusting the regex pattern to match the format of the MAC address in your output
        result = re.search(r"(\w\w-\w\w-\w\w-\w\w-\w\w-\w\w)", arp_output)
        if result:
            return result.groups()[0]
        else:
            return "MAC Address not found"
    except subprocess.CalledProcessError:
        return "No ARP entry found"

def ping_range(start_ip, end_ip):
    start_ip = ipaddress.IPv4Address(start_ip)
    end_ip = ipaddress.IPv4Address(end_ip)
    for ip_int in range(int(start_ip), int(end_ip) + 1):
        ip = str(ipaddress.IPv4Address(ip_int))
        if ping_ip(ip):
            print(f"IP: {ip} is up, MAC Address: {get_mac_address(ip)}")
        else:
            print(f"IP: {ip} is down")  

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ping a range of IP addresses and retrieve their MAC addresses.')
    parser.add_argument('start_ip', type=str, help='Start IP address (e.g., 10.0.0.1)')
    parser.add_argument('end_ip', type=str, help='End IP address (e.g., 10.0.0.255)')

    args = parser.parse_args()

    ping_range(args.start_ip, args.end_ip)
