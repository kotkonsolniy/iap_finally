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
        self.src_address = ipaddress.ip_address(self.src)
        self.dst_address = ipaddress.ip_address(self.dst)

        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except Exception:
            self.protocol = str(self.protocol_num)


class ICMP:
    def __init__(self, buff):
        # ICMP заголовок: тип (1 байт), код (1 байт), контрольная сумма (2 байта)
        header = struct.unpack("bbH", buff[:4])
        self.type = header[0]
        self.code = header[1]
        self.checksum = header[2]

        self.type_map = {
            0: "Echo Reply",
            3: "Destination Unreachable",
            4: "Source Quench",
            5: "Redirect",
            8: "Echo Request",
            11: "Time Exceeded",
            12: "Parameter Problem",
            13: "Timestamp",
            14: "Timestamp Reply",
            17: "Address Mask Request",
            18: "Address Mask Reply"
        }
        self.type_desc = self.type_map.get(self.type, "Unknown")


def sniff(host):
    if os.name == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((host, 0))

    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    try:
        while True:
            raw_buffer = sniffer.recvfrom(65535)[0]

            ip_header = IP(raw_buffer[0:20])

            print(f'Protocol: {ip_header.protocol} {ip_header.src_address} -> {ip_header.dst_address}')

            if ip_header.protocol == "ICMP":
                # смещение на длину IP-заголовка для ICMP
                offset = ip_header.ihl * 4
                icmp_header = ICMP(raw_buffer[offset:offset+4])
                print(f'    ICMP -> Type: {icmp_header.type} ({icmp_header.type_desc}), Code: {icmp_header.code}')

    except KeyboardInterrupt:
        if os.name == 'nt':
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        sys.exit()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        host = '192.168.0.104'
    sniff(host)
