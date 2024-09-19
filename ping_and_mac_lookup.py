import os
import subprocess
import ipaddress
import re
import argparse


def ping_ip(ip):
    try:
        subprocess.check_output(["ping", "-n", "1", ip], stderr=subprocess.STDOUT, universal_newlines=True)
        return True
    except subprocess.CalledProcessError:
        return False


def get_mac_address(ip):
    try:
        arp_output = subprocess.check_output(['arp', '-a', ip], universal_newlines=True)
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
    parser = argparse.ArgumentParser(description='Ping a range of IP addresses and lookup their MAC addresses.')
    parser.add_argument('start_ip', type=str, help='The starting IP address of the range.')
    parser.add_argument('end_ip', type=str, help='The ending IP address of the range.')

    args = parser.parse_args()

    ping_range(args.start_ip, args.end_ip)