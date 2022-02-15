from scapy.all import *
import sys
destination = sys.argv[1]
i = 1
while True:
    packet = IP(ttl=i,dst=destination)/ICMP()
    try:
        res = sr1(packet, verbose=0, timeout=2)
        print(res[IP].src)
        if res[ICMP].type == 0:
            break
    except:
        print("no response")
    i+=1