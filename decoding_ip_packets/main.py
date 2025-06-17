import struct
import ipaddress

class IP:
    def __init__(self, raw_data):
        # Распаковываем первые 20 байт IP-заголовка
        # Формат:
        # B  - 1 байт (Version + IHL)
        # B  - 1 байт (TOS)
        # H  - 2 байта (Total Length)
        # H  - 2 байта (Identification)
        # H  - 2 байта (Flags + Fragment Offset)
        # B  - 1 байт (TTL)
        # B  - 1 байт (Protocol)
        # H  - 2 байта (Header checksum)
        # 4s - 4 байта (Source IP)
        # 4s - 4 байта (Destination IP)
        ip_header = struct.unpack('!BBHHHBBH4s4s', raw_data[:20])

        # Версия IP - старшие 4 бита первого байта
        self.version = ip_header[0] >> 4
        # Длина заголовка (IHL) - младшие 4 бита первого байта, количество 32-битных слов
        self.ihl = ip_header[0] & 0xF
        # TOS (Type of Service)
        self.tos = ip_header[1]
        # Общая длина пакета (включая заголовок и данные)
        self.total_length = ip_header[2]
        # Идентификатор пакета
        self.identification = ip_header[3]
        # Флаги и смещение фрагмента (3 бита флагов + 13 битов смещения)
        self.flags_fragment_offset = ip_header[4]
        # Время жизни (TTL)
        self.ttl = ip_header[5]
        # Протокол (TCP=6, UDP=17, ICMP=1 и др.)
        self.protocol = ip_header[6]
        # Контрольная сумма заголовка
        self.header_checksum = ip_header[7]
        # IP-адрес источника (4 байта)
        self.src = ipaddress.ip_address(ip_header[8])
        # IP-адрес назначения (4 байта)
        self.dst = ipaddress.ip_address(ip_header[9])

        # Флаги — выделяем 3 старших бита из flags_fragment_offset (16 бит)
        self.flags = (self.flags_fragment_offset >> 13) & 0x7
        # Смещение фрагмента — младшие 13 бит
        self.fragment_offset = self.flags_fragment_offset & 0x1FFF

    def __str__(self):
        return (f"IP Packet:\n"
                f" Version: {self.version}\n"
                f" Header Length: {self.ihl * 4} bytes\n"
                f" Type of Service: {self.tos}\n"
                f" Total Length: {self.total_length}\n"
                f" Identification: {self.identification}\n"
                f" Flags: {bin(self.flags)}\n"
                f" Fragment Offset: {self.fragment_offset}\n"
                f" TTL: {self.ttl}\n"
                f" Protocol: {self.protocol}\n"
                f" Header Checksum: {hex(self.header_checksum)}\n"
                f" Source IP: {self.src}\n"
                f" Destination IP: {self.dst}")

# Пример использования
if __name__ == "__main__":
    # Пример сырых данных IP-пакета (20 байт IP заголовка)
    # Обычно такие данные получаются из сырого сокета
    sample_raw_ip = b'\x45\x00\x00\x3c\x1c\x46\x40\x00\x40\x06\xa6\xec\xc0\xa8\x01\x64\xc0\xa8\x01\xc8'
    ip_packet = IP(sample_raw_ip)
    print(ip_packet)
