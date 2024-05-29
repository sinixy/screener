from scapy.all import sniff, Raw
from scapy.layers.l2 import Ether
from datetime import datetime

from struct import unpack


def bytes_to_price(byte_sequence):
    m_price = int.from_bytes(byte_sequence, byteorder='little')
    m_price = unpack('<I', byte_sequence)
    
    dollar_mask = (1 << 18) - 1
    dollars = (m_price >> 14) & dollar_mask
    
    fraction_mask = (1 << 14) - 1
    fraction = m_price & fraction_mask
    
    fraction_as_decimal = fraction / 10000.0
    
    price = dollars + fraction_as_decimal
    
    return price

def show_prints(packet: Ether):
    if Raw not in packet:
        return
    
    data = packet[Raw].load
    message_length, message_type = unpack('<HH', data[:4])

    # print(f'len={message_length} | type={message_type}')
    if message_type == 5:
        time = datetime.fromtimestamp(
            datetime.today().replace(hour=0, minute=0, second=0, microsecond=0).timestamp() + unpack('<I', data[4:8])[0] / 1000
        )
        symbol = str(data[8:16]).replace('\\x00', '')
        shares = unpack('<I', data[32:36])[0]
        print(f'type={message_type} | time={time} | symbol={symbol} | shares={shares}')

        # i = 16
        # while i <= message_length - 4:
        #     print(f'{unpack("<I", data[i:i+4])[0]} -> {i}:{i+4}', end=' | ')
        #     i += 1
    elif message_type == 8:
        time = datetime.fromtimestamp(
            datetime.today().replace(hour=0, minute=0, second=0, microsecond=0).timestamp() + unpack('<I', data[4:8])[0] / 1000
        )
        symbol = str(data[8:16]).replace('\\x00', '')
        price_dollars, price_fraction, match_number, shares = unpack(f'<IIQI', data[16:36])
        print(f'type={message_type} | time={time} | symbol={symbol} | shares={shares} | price={price_dollars}.{price_fraction}')

def show_book(packet: Ether):
    if Raw not in packet:
        return
    
    data = packet[Raw].load
    message_length, message_type = unpack('<HH', data[:4])
    if message_type == 2:
        symbol = str(data[4:12]).replace('\\x00', '')
        side, referenceNumber, price_dollars, price_fraction, size, mmid, millisecond, bookID, quoteCondition, flags = unpack('<BxxxQIIIIIBBH', data[12:48])
        print(f'type={message_type} | symbol={symbol} | shares={size} | cond={quoteCondition} | price={price_dollars}.{price_fraction}\n')


def show_sorter(packet: Ether):
    if Raw not in packet:
        return
    
    data = packet[Raw].load
    message_length, message_type = unpack('<HH', data[:4])
    if 'NVDA' in str(data) and message_type == 503:
        symbol = str(data[4:12]).replace('\\x00', '')
        price, size = unpack('<IH', data[12:18])
        print(message_length, len(data), symbol, price, size)
        # print(data, '\n')

unique_types = []

def show_test(packet: Ether):
    if Raw not in packet:
        return
    
    data = packet[Raw].load
    message_length, message_type = unpack('<HH', data[:4])
    if str(message_type)[:2] == '17':
        print(f'type={message_type} | length={message_length} | alen={len(data)}')
        print(data)

capture = sniff(filter='ip src 185.41.250.207', prn=show_test)