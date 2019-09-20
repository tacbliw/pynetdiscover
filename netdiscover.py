#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import struct
import ifaddr
import ipaddress
from pprint import pprint
import uuid

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
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
    sock.bind('eth0', 0)

    for addr in addresses:
        data = packet_builder()

def packet_builder(addr):
    """Build an ARP packet with the IP address, return bytes"""
    packet = b''
    # Ethernet header
    packet += b'\xff\xff\xff\xff\xff\xff'  # broadcast MAC address
    packet += struct.pack('!')
    packet += struct.pack('!H', 0x0806)

    # ARP message
    packet += struct.pack('!H', 0x0001)  # Hardware type (HTYPE)
    packet += struct.pack('!H', 0x0800)  # Protocol type (PTYPE)
    packet += struct.pack('!B', 0x0006)  # Hardware address length (HLEN)
    packet += struct.pack('!B', 0x0004)  # Protocol address length (PLEN)
    packet += struct.pack('!B', 0x0001)  # Operation (OPER)
    packet += struct.pack()

def send_packet(sock, data):
    sock.send(data)

def recv_packet(sock):
    sock.recv(1024)

if __name__ == '__main__':
    run()
