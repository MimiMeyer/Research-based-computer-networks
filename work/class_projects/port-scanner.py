from scapy.all import*

server_ip = 'www.google.com'
start_port = 75
end_port = 84
syn_flag = 0x2
synack_flag = 0x12


open_ports = []
p = IP(dst=server_ip)/TCP(flags=syn_flag)

for port in range(start_port,end_port+1):
    p[TCP].dport = port
    print('Testing port: {}'.format(port))
    r = sr1(p, timeout=0.2, verbose=False)
    try:
        if r[TCP].flags == synack_flag:
            print('Found open port: {}'.format(port))
            open_ports.append(port)
    except:
        pass
    print(open_ports)