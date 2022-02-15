# targil in scapy Mimi Meyer 317924835
import sys
i, o, e = sys.stdin, sys.stdout, sys.stderr
from scapy.all import *
sys.stdin, sys.stdout, sys.stderr = i, o, e
import socket
type_ptr = "-type=PTR"  # use it twice
dst_ip = '8.8.8.8'  # google dns server
ptr = 12
cname = 5
a = 1


def reverse_mapping(response):
    """ reverses the ip if its valid and sends dns packet """
    if response[1] == type_ptr and len(response) == 3:
        try:
            socket.inet_aton(response[2])  # checking if its a valid ip
            # need to reverse the ip in order to use as qname
            reverse_ip = ".".join(reversed(response[2].split('.'))) + '.in-addr.arpa.'
            dns_packet = IP(dst=dst_ip) / UDP(sport=24601, dport=53) / DNS(qdcount=1, rd=1) / DNSQR(qname=reverse_ip, qtype=ptr)
            response_packet = sr1(dns_packet)  # sending and receiving an answer
            print_query_data(response_packet)
        except socket.error:
            print("Not a legal IP")
    else:
        print("Illegal parameters")

    return


def domain(response):
    """gets the domain name and sends dns packet """
    domain_name = response[1]
    if "." in domain_name and len(response) == 2:
        dns_packet = IP(dst=dst_ip) / UDP(sport=24601, dport=53) / DNS(qdcount=1, rd=1) / DNSQR(qname=domain_name)
        response_packet = sr1(dns_packet)  # sending and receiving an answer
        print_query_data(response_packet)
    else:
        print('not a valid domain name')
    return


def print_query_data(dns_packet):
    """checks how many answers and prints according to type"""
    length = dns_packet[DNS].ancount  # the number of answers
    if length > 0:  # has answers
        a_count, cname_count = 0, 0
        for j in range(length):
            if dns_packet[DNSRR][j].type == cname:  # type CNAME
                if cname_count == 0:  # the first one of type cname
                    print("Aliases: ")
                    cname_count += 1
                print(dns_packet[DNSRR][j].rdata.decode())
            if dns_packet[DNSRR][j].type == a:  # type A
                if a_count == 0:  # the first one of type A
                    print("Addresses: ")  # printing the alias
                    a_count += 1
                print(dns_packet[DNSRR][j].rdata)  # printing the IP
            if dns_packet[DNSRR][j].type == ptr:  # type PTR
                print("name = " + dns_packet[DNSRR][j].rdata.decode())  # printing the name of the wanted ip
    else:
        print("UnKnown domain can't find or no answer")  # has not received an answer
    return


def main():
    """gets the parameter and decides where to send it too"""
    response = sys.argv  # getting the parameters
    if len(sys.argv) != 1:  # if there are parameters
        if type_ptr in sys.argv:  # if it contains -type=PTR
            reverse_mapping(response)
        else:
            domain(response)
    else:
        print("You must enter a parameter")


if __name__ == "__main__":
    main()
