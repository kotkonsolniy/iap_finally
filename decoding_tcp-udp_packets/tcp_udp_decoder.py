import struct
import socket


def decode_ip_header(data):
    """
    Декодирует IP-заголовок из первых 20 байт данных
    Возвращает словарь с полями заголовка
    """
    # Распаковываем первые 20 байт (базовый заголовок без опций)
    fields = struct.unpack('!BBHHHBBH4s4s', data[:20])

    # Извлекаем отдельные поля
    version_ihl = fields[0]
    tos = fields[1]
    total_length = fields[2]
    identification = fields[3]
    flags_fragment = fields[4]
    ttl = fields[5]
    protocol = fields[6]
    checksum = fields[7]
    src_ip_bytes = fields[8]
    dst_ip_bytes = fields[9]

    # Вычисляем версию и длину заголовка
    version = version_ihl >> 4
    ihl = version_ihl & 0x0F
    header_length = ihl * 4  # в байтах

    # Извлекаем флаги и смещение фрагмента
    flags = flags_fragment >> 13
    fragment_offset = flags_fragment & 0x1FFF

    # Преобразуем IP-адреса в строковый формат
    src_ip = socket.inet_ntoa(src_ip_bytes)
    dst_ip = socket.inet_ntoa(dst_ip_bytes)

    return {
        'version': version,
        'header_length': header_length,
        'tos': tos,
        'total_length': total_length,
        'identification': identification,
        'flags': flags,
        'fragment_offset': fragment_offset,
        'ttl': ttl,
        'protocol': protocol,
        'checksum': checksum,
        'src_ip': src_ip,
        'dst_ip': dst_ip
    }


def decode_tcp_header(data):
    """
    Декодирует TCP-заголовок из первых 20 байт данных
    Возвращает словарь с полями заголовка
    """
    # Распаковываем первые 20 байт (базовый заголовок без опций)
    fields = struct.unpack('!HHLLBBHHH', data[:20])

    # Извлекаем отдельные поля
    sport = fields[0]
    dport = fields[1]
    seq_num = fields[2]
    ack_num = fields[3]
    offset_reserved = fields[4]
    flags = fields[5]
    window_size = fields[6]
    checksum = fields[7]
    urg_ptr = fields[8]

    # Вычисляем длину заголовка и зарезервированные биты
    data_offset = (offset_reserved >> 4) * 4  # в байтах
    reserved = offset_reserved & 0x0F

    # Разбираем флаги (каждый бит - отдельный флаг)
    urg = (flags & 0x20) >> 5
    ack = (flags & 0x10) >> 4
    psh = (flags & 0x08) >> 3
    rst = (flags & 0x04) >> 2
    syn = (flags & 0x02) >> 1
    fin = flags & 0x01

    return {
        'sport': sport,
        'dport': dport,
        'seq_num': seq_num,
        'ack_num': ack_num,
        'data_offset': data_offset,
        'reserved': reserved,
        'flags': {
            'URG': bool(urg),
            'ACK': bool(ack),
            'PSH': bool(psh),
            'RST': bool(rst),
            'SYN': bool(syn),
            'FIN': bool(fin)
        },
        'window_size': window_size,
        'checksum': checksum,
        'urg_ptr': urg_ptr
    }


def decode_udp_header(data):
    """
    Декодирует UDP-заголовок из первых 8 байт данных
    Возвращает словарь с полями заголовка
    """
    # Распаковываем весь UDP-заголовок (8 байт)
    sport, dport, length, checksum = struct.unpack('!HHHH', data[:8])

    return {
        'sport': sport,
        'dport': dport,
        'length': length,
        'checksum': checksum
    }


def decode_packet(raw_data):
    """
    Декодирует полный сетевой пакет (IP + транспортный уровень)
    """
    # Декодируем IP-заголовок
    ip_header = decode_ip_header(raw_data)

    # Определяем начало транспортного заголовка
    transport_start = ip_header['header_length']
    transport_data = raw_data[transport_start:]

    # Декодируем транспортный протокол
    if ip_header['protocol'] == 6:  # TCP
        tcp_header = decode_tcp_header(transport_data)
        payload_start = transport_start + tcp_header['data_offset']
        payload = raw_data[payload_start:]

        print("=== TCP Packet ===")
        print(f"Source: {ip_header['src_ip']}:{tcp_header['sport']}")
        print(f"Destination: {ip_header['dst_ip']}:{tcp_header['dport']}")
        print(f"Flags: {', '.join([f for f, v in tcp_header['flags'].items() if v])}")
        print(f"Payload size: {len(payload)} bytes")

    elif ip_header['protocol'] == 17:  # UDP
        udp_header = decode_udp_header(transport_data)
        payload = raw_data[transport_start + 8:]

        print("=== UDP Packet ===")
        print(f"Source: {ip_header['src_ip']}:{udp_header['sport']}")
        print(f"Destination: {ip_header['dst_ip']}:{udp_header['dport']}")
        print(f"Payload size: {len(payload)} bytes")

    else:
        print(f"Unsupported protocol: {ip_header['protocol']}")


# Пример использования
if __name__ == "__main__":
    # Создаем тестовый TCP-пакет
    # IP-заголовок (20 байт) + TCP-заголовок (20 байт)
    raw_packet = bytes.fromhex(
        '45 00 00 34 12 34 40 00 40 06 00 00 7f 00 00 01'  # IP-заголовок
        '7f 00 00 01 04 d2 00 50 00 00 00 01 00 00 00 02'  # TCP-заголовок
        '50 10 00 00 00 00 00 00'  # TCP-заголовок (продолжение)
    )

    decode_packet(raw_packet)