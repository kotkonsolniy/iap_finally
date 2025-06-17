import sys  # Работа с системными параметрами и выходом из программы
import ipaddress  # Удобная работа с IP-адресами
import socket  # Работа с сетевыми сокетами
import os  # Работа с ОС и её функциями
import struct  # Разбор бинарных данных (упаковка/распаковка)


class IP:
    def __init__(self, buff=None):
        # Распаковываем первые 20 байт IP-заголовка в поля согласно формату
        # '<' — little-endian, 'B' — unsigned char, 'H' — unsigned short, '4s' — 4 байта строка
        header = struct.unpack("<BBHHHBBH4s4s", buff)

        # Версия IP (старшие 4 бита первого байта)
        self.ver = header[0] >> 4

        # Длина IP-заголовка (младшие 4 бита первого байта)
        self.ihl = header[0] & 0xF

        # Тип сервиса (QoS)
        self.tos = header[1]

        # Общая длина пакета (заголовок + данные)
        self.len = header[2]

        # Идентификатор пакета
        self.id = header[3]

        # Смещение фрагмента
        self.offset = header[4]

        # Время жизни (TTL)
        self.ttl = header[5]

        # Номер протокола (TCP=6, UDP=17, ICMP=1 и т.д.)
        self.protocol_num = header[6]

        # Контрольная сумма заголовка
        self.sum = header[7]

        # IP-адрес источника (4 байта)
        self.src = header[8]

        # IP-адрес назначения (4 байта)
        self.dst = header[9]

        # Преобразуем IP-адреса из бинарного формата в читабельный (например, '192.168.0.1')
        self.src_address = ipaddress.ip_address(self.src)
        self.dst_address = ipaddress.ip_address(self.dst)

        # Сопоставление номера протокола с его названием для удобства вывода
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
        try:
            # Если номер протокола известен — выводим его название
            self.protocol = self.protocol_map[self.protocol_num]
        except Exception:
            # Если нет — выводим число как строку
            self.protocol = str(self.protocol_num)


class ICMP:
    def __init__(self, buff):
        # ICMP-заголовок состоит из: тип (1 байт), код (1 байт), контрольная сумма (2 байта)
        # Распаковываем первые 4 байта ICMP-заголовка
        header = struct.unpack("bbH", buff[:4])

        # Тип ICMP-сообщения (например, Echo Request, Destination Unreachable)
        self.type = header[0]

        # Код сообщения, уточняющий тип
        self.code = header[1]

        # Контрольная сумма ICMP-пакета
        self.checksum = header[2]

        # Сопоставление типов ICMP с описанием для удобства
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
        # Получаем описание типа, если оно есть, иначе "Unknown"
        self.type_desc = self.type_map.get(self.type, "Unknown")


def sniff(host):
    # Для Windows используем IPPROTO_IP, для Linux — IPPROTO_ICMP (захват ICMP пакетов)
    if os.name == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    # Создаём сырой сокет для захвата IP-пакетов
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

    # Привязываем сокет к интерфейсу с указанным IP (host) и произвольному порту 0
    sniffer.bind((host, 0))

    # Устанавливаем опцию, чтобы включить IP-заголовок в перехваченные данные
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    # Если ОС Windows — включаем режим захвата всех пакетов
    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    try:
        while True:
            # Получаем сырые данные пакета (максимум 65535 байт)
            raw_buffer = sniffer.recvfrom(65535)[0]

            # Создаём объект IP, передавая первые 20 байт для анализа заголовка
            ip_header = IP(raw_buffer[0:20])

            # Выводим протокол и IP адреса отправителя и получателя
            print(f'Protocol: {ip_header.protocol} {ip_header.src_address} -> {ip_header.dst_address}')

            # Если протокол ICMP, то декодируем и выводим тип и код ICMP
            if ip_header.protocol == "ICMP":
                # Определяем длину IP-заголовка (ihl — число 32-битных слов, умножаем на 4 для байт)
                offset = ip_header.ihl * 4

                # Извлекаем ICMP-заголовок (4 байта после IP-заголовка)
                icmp_header = ICMP(raw_buffer[offset:offset + 4])

                # Выводим тип, описание и код ICMP-сообщения
                print(f'    ICMP -> Type: {icmp_header.type} ({icmp_header.type_desc}), Code: {icmp_header.code}')

    except KeyboardInterrupt:
        # При нажатии Ctrl+C — выключаем режим захвата пакетов на Windows и выходим
        if os.name == 'nt':
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        sys.exit()


if __name__ == '__main__':
    # Если передан IP в аргументах командной строки — используем его, иначе — IP по умолчанию
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        host = '192.168.0.104'  # поменяй на IP своего интерфейса, если нужно
    sniff(host)
