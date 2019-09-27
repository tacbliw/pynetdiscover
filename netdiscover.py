#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import struct
import ifaddr
import ipaddress
import fcntl
from pprint import pprint

def run():
    IFACE = ''
    adapters = list(ifaddr.get_adapters())

    print("Choose an adapter:")
    for i in range(len(adapters)):
        print("{0:>2}) [{1:>18}] {2}".format(i, adapters[i].ips[0].ip + '/' + str(adapters[i].ips[0].network_prefix), adapters[i].nice_name))

    choice = int(input(">>> "))
    if choice in range(len(adapters)):
        IFACE = adapters[choice].nice_name
        print("Your choice: " + IFACE)
    else:
        print("Choice not in range.")
        exit(1)

    ip = adapters[choice].ips[0].ip
    network_prefix = adapters[choice].ips[0].network_prefix

    # List all address to scan
    addresses = ipaddress.ip_network(ip + '/' + str(network_prefix), strict=False).hosts()

    # Create socket
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
    sock.bind((IFACE, 0))

    for addr in addresses:
        data = packet_builder()

def get_hw_address(ifname):
    """Return bytes of MAC address of an interface"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', ifname[:15].encode('ascii')))
    return info[18:24]
    
def get_ip_address(ifname):
    """Return bytes of IP address of an interface"""

    
def packet_builder(src_addr, des_addr, mac):
    """Build an ARP packet with the IP address, return bytes"""
    packet = b''
    # Ethernet header
    packet += b'\xff\xff\xff\xff\xff\xff'  # broadcast MAC address
    packet += mac
    packet += struct.pack('!H', 0x0806)

    # ARP message
    packet += struct.pack('!H', 0x0001)  # Hardware type (HTYPE)
    packet += struct.pack('!H', 0x0800)  # Protocol type (PTYPE)
    packet += struct.pack('!B', 0x0006)  # Hardware address length (HLEN)
    packet += struct.pack('!B', 0x0004)  # Protocol address length (PLEN)
    packet += struct.pack('!B', 0x0001)  # Operation (OPER)
    packet += mac  # Sender hardware address (SHA)
    packet += struct.pack('!', )
    packet += b'\x00\x00\x00\x00\x00\x00'  # Target hardware address (THA)
    packet += struct.pack('', )

def send_packet(sock, data):
    sock.send(data)

def recv_packet(sock):
    sock.recv(1024)

if __name__ == '__main__':
    run()
