from scapy.all import *
p = IP(dst='8.8.8.8',ttl=1)/ICMP()/Raw(load='hello cyber women!') # ttl is optinal
p.show()
r = sr1(p, verbose=0, timeout = 1)  # verbose is for the dots
