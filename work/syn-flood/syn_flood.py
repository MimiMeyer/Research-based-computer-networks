# targil syn_flood Miriam Meyer 317924835
from scapy.all import *

pcap_filename = "SynFloodSample.pcap"
SYN = 0x02
ACK = 0x10
SYNACK = 0x12
time_to_wait = 0.004  # saw on wireshark that it was the shortest time between packets other then zero


# condition- syn ack without ack
def syn_ack_without_ack(pcap_file):
    """goes through packets and adds whatever ips get a syn ack but donsn't return an ack to a list and returns it"""
    suspicious_ip1 = []  # list for suspicious ip
    for pkt in pcap_file:
        if TCP in pkt:
            if pkt[TCP].flags == SYNACK:
                seq_num = pkt[TCP].seq  # saving the seq num
                ack_num = pkt[TCP].ack  # saving the ack num
                ip = pkt[IP].dst  # saving the ip
                count = 0  # help to see if ack was sent
                for pkt1 in pcap_file:  # going over the packets again to see if it got an ack
                    if TCP in pkt1:
                        if pkt1[TCP].flags == ACK:  # ack packet
                            if pkt[IP].src == ip and pkt1[TCP].seq == ack_num and pkt1[TCP].ack == seq_num + 1:
                                # if it's the ip that got a syn ack and sent a proper ack back
                                count += 1
                if count == 0:  # there was no proper ack sent
                    suspicious_ip1.append(ip)  # add to list of suspicious ips
    return suspicious_ip1


# condition-fast syn's
def fast_syns(pcap_file):
    """ goes through packets and adds whatever ips are sending syns too fast to a list and returns it """
    suspicious_ip2 = []  # list for suspicious ip
    ack_packets = {}  # dict for ip and there times
    for pkt in pcap_file:  # going over packets
        if TCP in pkt:
            if pkt[TCP].flags == SYN:  # syn packet
                ip_src = pkt[IP].src  # getting wanted ip
                if ip_src in ack_packets:
                    # check if delta time is big enough
                    if pkt.time - ack_packets[pkt[IP].src] < time_to_wait:
                        # not big enough- suspicious add ip_src to list if it doesnt already exist
                        if ip_src not in suspicious_ip2:
                            suspicious_ip2.append(ip_src)
                    else:
                        # big enough- update dict value with current time
                        ack_packets.update(ip=pkt.time)
                else:
                    ack_packets[ip_src] = pkt.time  # add dict value
    return suspicious_ip2


def write_to_file(ip_file, my_list):
    """writes the ip into file"""
    for ip in my_list:
        ip_file.write(ip + "\n")
    return


def main():
    """creates file, opens the pcap file and calls the needed functions"""
    attackers_list_file = open('attackersListFiltered.text', 'w')
    pcap_file = rdpcap(pcap_filename)  # open pcap file
    print("opened")
    sp1 = syn_ack_without_ack(pcap_file)
    sp2 = fast_syns(pcap_file)
    write_to_file(attackers_list_file, sp1+sp2)


if __name__ == "__main__":
    main()
