import sys
import ipaddress
import socket
import os
import struct


class IP:
    def __init__(self, buff=None):
        header = struct.unpack("<BBHHHBBH4s4s", buff)
        self.ver = header[0] >> 4
        self.ihl = header[0] & 0xF
        self.tos = header[1]
        self.len = header[2]
        self.id = header[3]
        self.offset = header[4]
        self.ttl = header[5]
        self.protocol_num = header[6]
        self.sum = header[7]
        self.src = header[8]
        self.dst = header[9]
        # IP-адреса, понятные человеку
        self.src_address = ipaddress.ip_address(self.src)
        self.dst_address = ipaddress.ip_address(self.dst)
        # сопоставляем константы протоколов с их названиями
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except Exception as e:
            print('%s No protocol for %s' % (e, self.protocol_num))
            self.protocol = str(self.protocol_num)

def sniff(host):
    # должно быть знакомо по предыдущему примеру
    if os.name == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(
        socket.AF_INET,
        socket.SOCK_RAW, socket_protocol
    )
    sniffer.bind((host, 0))
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    try:
        while True:
            # читаем пакет
            raw_buffer = sniffer.recvfrom(65535)[0]

            # создаём IP-заголовок из первых 20 байтов
            ip_header = IP(raw_buffer[0:20])
            # выводим обнаруженные протокол и адреса
            print(
                'Protocol: %s %s -> %s' % (
                    ip_header.protocol,
                    ip_header.src_address,
                    ip_header.dst_address
                )
            )
    except KeyboardInterrupt:
        # если мы в виндоус, то отключаем неизбирательный режим
        if os.name == 'nt':
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        sys.exit()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        host = '192.168.23.221'
    sniff(host)