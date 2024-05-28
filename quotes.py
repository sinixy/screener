from scapy.all import sniff, Raw
from scapy.layers.l2 import Ether

from struct import unpack


def pprint(packet: Ether):
    if Raw not in packet:
        return
    
    data = packet[Raw].load
    message_length, message_type = unpack('<HH', data[:4])
    if message_type == 14:
        print(data)
    print(message_length, message_type)
    

capture = sniff(filter='ip src 185.41.250.207', prn=pprint)