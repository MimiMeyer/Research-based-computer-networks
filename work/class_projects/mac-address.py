from scapy.all import *
network_id = '192.168.214.'
for i in range(255):
    destination = network_id + str(i)
    p = ARP(pdst=destination)
    try:
        r = sr1(p, verbose=0, timeout= 0.1)
        print(str(r[ARP].hwsrc), str(r[ARP].psrc))
    except:
        print(i)