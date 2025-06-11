import ipaddress


def calculate_network(ip_address, subnet_mask):
    """
    Вычисляет сетевой адрес по IP-адресу и маске подсети
    с использованием библиотеки ipaddress
    """
    interface = ipaddress.IPv4Interface(f"{ip_address}/{subnet_mask}")
    return str(interface.network.network_address)


def calculate_broadcast(ip_address, subnet_mask):
    """
    Вычисляет широковещательный адрес
    """
    network = ipaddress.IPv4Network(f"{ip_address}/{subnet_mask}", strict=False)
    return str(network.broadcast_address)


def get_ip_class(ip_address):
    """
    Определяет класс IP-адреса
    """
    ip = ipaddress.IPv4Address(ip_address)
    first_octet = int(ip.packed[0])

    if ip.is_multicast:
        return "D (Multicast)"
    elif ip.is_private:
        return "Private"
    elif ip.is_reserved:
        return "E (Experimental)"
    elif first_octet < 128:
        return "A"
    elif first_octet < 192:
        return "B"
    elif first_octet < 224:
        return "C"


def cidr_to_mask(cidr):
    """
    Конвертирует CIDR-нотацию в маску подсети
    """
    return str(ipaddress.IPv4Network(f"0.0.0.0/{cidr}").netmask)


def subnet_info(ip_with_cidr):
    """
    Полная информация о подсети
    """
    network = ipaddress.IPv4Network(ip_with_cidr, strict=False)
    return {
        "network_address": str(network.network_address),
        "broadcast_address": str(network.broadcast_address),
        "netmask": str(network.netmask),
        "hostmask": str(network.hostmask),
        "prefixlen": network.prefixlen,
        "num_addresses": network.num_addresses,
        "usable_hosts": list(network.hosts())[:5]  # Первые 5 доступных адресов
    }


# Пример использования
if __name__ == "__main__":
    ip = "192.168.1.10"
    cidr = 24

    print(f"IP-адрес: {ip}")
    print(f"Маска для /{cidr}: {cidr_to_mask(cidr)}")
    print(f"Сетевой адрес: {calculate_network(ip, cidr_to_mask(cidr))}")
    print(f"Широковещательный адрес: {calculate_broadcast(ip, cidr_to_mask(cidr))}")
    print(f"Класс адреса: {get_ip_class(ip)}")

    # Полная информация о подсети
    full_info = subnet_info("192.168.1.0/24")
    print("\nПолная информация о подсети:")
    for key, value in full_info.items():
        print(f"{key:>18}: {value}")

    # Проверка принадлежности адреса к подсети
    network = ipaddress.IPv4Network("192.168.1.0/24")
    print(f"\nАдрес 192.168.1.42 в подсети: {ipaddress.IPv4Address('192.168.1.42') in network}")
    print(f"Адрес 192.168.2.42 в подсети: {ipaddress.IPv4Address('192.168.2.42') in network}")