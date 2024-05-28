from scapy.all import sniff, Raw
from scapy.layers.l2 import Ether
from datetime import datetime

from struct import unpack


def pprint(packet: Ether):
    if Raw not in packet:
        return
    
    data = packet[Raw].load
    message_length, message_type = unpack('<HH', data[:4])
    if message_type == 5:
        print(f'len={message_length} | type={message_type}')
        time = datetime.fromtimestamp(
            datetime.today().replace(hour=0, minute=0, second=0, microsecond=0).timestamp() + unpack('<I', data[4:8])[0] / 1000
        )
        symbol = str(data[8:16]).replace('\\x00', '')
        shares = unpack('<I', data[32:36])[0]
        print(f'time={time} | symbol={symbol} | shares={shares}')

        # i = 16
        # while i <= message_length - 4:
        #     print(f'{unpack("<I", data[i:i+4])[0]} -> {i}:{i+4}', end=' | ')
        #     i += 1

        print(data)
    

capture = sniff(filter='ip src 185.41.250.207', prn=pprint)