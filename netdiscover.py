#!/usr/bin/python

import socket
import struct
import ifaddr
import ipaddress
from pprint import pprint

def run():
    adapters = list(ifaddr.get_adapters())

    print("Choose an adapter:")
    for i in range(len(adapters)):
        print("{0:>2}) [{1:>18}] {2}".format(i, adapters[i].ips[0].ip + '/' + str(adapters[i].ips[0].network_prefix), adapters[i].nice_name))

    choice = int(input(">>> "))
    if choice in range(len(adapters)):
        print("Your choice: " + adapters[choice].nice_name)
    else:
        print("Choice not in range.")
        exit(1)

    ip = adapters[choice].ips[0].ip
    network_prefix = adapters[choice].ips[0].network_prefix

    # List all address to scan
    addresses = ipaddress.ip_network(ip + '/' + str(network_prefix), strict=False).hosts()

    # Create socket
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.SOCK_RAW)

    for addr in addresses:
        data = packet_builder()

def packet_builder(addr):
    """Build an ARP packet with the IP address, return bytes"""
    pass

if __name__ == '__main__':
    run()
