#!/usr/bin/python

import socket
import struct
import ifaddr
import ipaddress
from pprint import pprint

adapters = ifaddr.get_adapters()

print("Choose an adapter:")
for i in range(len(adapters)):
    print("{0:>2}) [{1:>18}] {2}".format(i, adapters[i].ips[-1].ip + '/' + str(adapters[i].ips[-1].network_prefix), adapters[i].nice_name))

choice = int(input(">>> "))
if choice in range(len(adapters)):
    print("Your choice: " + adapters[choice].nice_name)
else:
    print("Choice not in range.")
    exit(1)

ip = adapters[choice].ips[-1].ip
network_prefix = adapters[choice].ips[-1].network_prefix

# List all address to scan
addresses = ipaddress.ip_network(ip + '/' + str(network_prefix), strict=False).hosts()
for i in range(10):
    print(repr(next(addresses)))
