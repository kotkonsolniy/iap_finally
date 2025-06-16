import socket
import struct
import argparse
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [SNIFFER] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler("sniffer.log"),
        logging.StreamHandler()
    ]
)

def ip_header_unpack(packet):
    # Первые 20 байт — заголовок IPv4
    ip_header = packet[0:20]
    iph = struct.unpack('!BBHHHBBH4s4s', ip_header)

    version_ihl = iph[0]
    version = version_ihl >> 4
    ihl = version_ihl & 0xF

    ttl = iph[5]
    protocol = iph[6]
    src_ip = socket.inet_ntoa(iph[8])
    dst_ip = socket.inet_ntoa(iph[9])

    return {
        "version": version,
        "header_length": ihl * 4,
        "ttl": ttl,
        "protocol": protocol,
        "source_ip": src_ip,
        "destination_ip": dst_ip
    }

def start_sniffer():
    try:
        # AF_INET для IPv4, SOCK_RAW для
