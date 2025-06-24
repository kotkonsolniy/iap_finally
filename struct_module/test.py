class IP:
    def __init__(self, raw_data):
        """
        Парсим IP-заголовок из raw данных.
        """
        # Распаковываем первые 20 байт
        ip_header = struct.unpack('!BBHHHBBH4s4s', raw_data[:20])

        self.version_ihl = ip_header[0]          # Версия + Internet Header Length
        self.version = self.version_ihl >> 4     # Версия (4 бита)
        self.ihl = self.version_ihl & 0xF        # Длина заголовка (4 бита)

        self.tos = ip_header[1]                  # Type of Service
        self.total_length = ip_header[2]         # Общая длина пакета
        self.identification = ip_header[3]       # ID пакета
        self.flags_offset = ip_header[4]         # Flags + Fragment Offset

        self.ttl = ip_header[5]                  # Time To Live
        self.protocol = ip_header[6]             # Протокол (TCP=6, UDP=17)
        self.checksum = ip_header[7]             # Контрольная сумма заголовка
        self.src_ip = socket.inet_ntoa(ip_header[8])   # IP отправителя
        self.dest_ip = socket.inet_ntoa(ip_header[9])  # IP получателя
