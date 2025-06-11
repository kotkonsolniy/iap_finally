Структуры в C++ позволяют хранить данные различных типов в одном объекте. Они удобны для объединения логически связанных данных.
структуры в с++ могут хранить различные типы данных

Объединение (`union`) в C++ похоже на структуру, но в отличие от неё, все поля используют одно и то же место в памяти. Это позволяет хранить разные представления данных, но в один момент времени использовать только одно поле. (пример - как записать ip. можно четыре раза по числу,  можно символами, по 4 байта, как-то ещё)

В языке C++ тип `char` может быть знаковым или беззнаковым. Это зависит от компилятора.

1. **Подписанный (`signed char`)**:
    
    - Диапазон значений: от **-128** до **127**
    - Может хранить отрицательные числа
2. **Беззнаковый (`unsigned char`)**:
    
    - Диапазон значений: от **0** до **255**
    - Используется для хранения байтовых данных, например, цветовых значений
3. **Просто `char`**:
    
    - По умолчанию может быть либо `signed char`, либо `unsigned char`, в зависимости от реализации компилятора.

Перечисления в C++ используются для создания именованных констант.
Перечисления (`enum`) используются для создания набора именованных значений, которые представляют собой целые числа. Это помогает сделать код более читаемым и удобным.

**Пример использования:**
Представьте, что у вас есть три состояния светофора:

- **Красный**
- **Желтый**
- **Зеленый**
Вместо того, чтобы использовать `0`, `1` и `2`, можно объявить перечисление:
`enum TrafficLight { RED, YELLOW, GREEN };`


**Little-endian и big-endian** — это два способа хранения данных в памяти компьютера. 
**Little-endian** — порядок, при котором **младший значимый байт (LSB) хранится по меньшему адресу**, а **старший значимый байт (MSB) — по большему**. 
**Big-endian** — порядок, при котором **старший байт числа хранится по меньшему адресу**, что интуитивно понятно при чтении слева направо. 

![[Pasted image 20250301152257.png]]

Struct, ctypes

https://docs.python.org/3/library/ctypes.html
https://docs.python.org/3/library/struct.html

Для просмотра:
ip a - linux
ipconfig - windows

```python
import socket  
import os  
from struct import *  
# узел для прослушивани  
HOST = "192.168.50.221" # берём наш активный адрес  
  
  
def main():  
    # создаём сырой сокет и привязываем к общедоступному интерфейсу  
    if os.name == 'nt':  
        socket_protocol = socket.IPPROTO_IP  
    else:  
        socket_protocol = socket.IPPROTO_ICMP  
  
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)  
    sniffer.bind((HOST, 1))  
  
    # делаем так, чтобы захватывался IP-заголовок  
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)  
    if os.name == 'nt':  
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)  
  
    # читаем один пакет  
    #print(unpack('>bhl',sniffer.recvfrom(65565)[0]))    print(sniffer.recvfrom(65565))  
  
    # если мы в Windows, выключаем неизбираетльный режим  
    if os.name == 'nt':  
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)  
  
  
if __name__ == '__main__':  
    main()
```

Расшифровываем вывод. (запускать программу с правами администратора)
Вывод:
(b'E\x00\x00)\x0b^@\x00\x80\x06\x00\x00\xc0\xa82\xdd\x05\xff\xffM\xca\xe2\x01\xbb\x8fp\x8eK\xbb\xe61\x1bP\x10\x02\x02\xf8\xed\x00\x00\x00', ('192.168.50.221', 0))
ip зашит в \xc0\xa82\xdd
hex/число/ascii
c0 = 192
a8 = 168
32 = 50 = 2
dd = 221

![[Pasted image 20250301133114.png]]

ffi - Интерфейс внешних функций (англ. Foreign Function Interface, FFI) — это механизм, с помощью которого программа, написанная на одном языке программирования, может вызывать подпрограммы, написанные на другом языке. FFI часто используется при вызовах из бинарной динамически подключаемой библиотеки.

struct - конвертация из с в питон и наоборот (типы, структуры, код и т.д.)


```python
from ctypes import Structure, c_ubyte, c_ushort, c_uint32  
import socket  
import struct  
  
  
class IP(Structure):  
    _fields_ = [  
        ("ihl", c_ubyte, 4),  
        ("version", c_ubyte, 4),  
        ("tos", c_ubyte, 8),  
        ("len", c_ushort, 16),  
        ("id", c_ushort, 16),  
        ("offset", c_ushort, 16),  
        ("ttl", c_ubyte, 8),  
        ("protocol_num", c_ubyte, 8),  
        ("sum", c_ushort, 16),  
        ("src", c_uint32, 32),  
        ("dst", c_uint32, 32),  
    ]  
  
    def __new__(cls, socket_buffer=None):  
        return cls.from_buffer_copy(socket_buffer)  
  
    def __init__(self, socket_buffer=None):  
        # human readable IP addresses  
        self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))  
        self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))
```

![[Pasted image 20250301141503.png]]
![[Pasted image 20250301141513.png]]
![[Pasted image 20250301141528.png]]


```python
import ipaddress  
import struct  
  
  
class IP:  
    def __init__(self, buff=None):  
        header = struct.unpack("<BBHHHBB4s4s", buff)  
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
        # IP адреса, понятные человеку  
        self.src_address = ipaddress.ip_address(self.src)  
        self.dst_address = ipaddress.ip_address(self.dst)  
        # сопоставляем константы протоколов с их названиями  
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
```

"<BBHHHBBR454s"

![[Pasted image 20250301144329.png]]
![[Pasted image 20250301144301.png]]

ICMP пробуем реализовать
![[Pasted image 20250301150029.png]]
![[Pasted image 20250301150039.png]]

Примерный код:
ctypes:
```python
from ctypes import Structure, c_ubyte, c_ushort, c_uint32  
import socket  
import struct  
  
  
class IP(Structure):  
    _fields_ = [  
        ("type", c_ubyte, 8),  
        ("code", c_ubyte, 8),  
        ("control_sum", c_ushort, 16),  
        ("id", c_ushort, 16),  
        ("number", c_ushort, 16),  
        ("additional_inf", c_uint32, 32),  
    ]  
  
    def __new__(cls, socket_buffer=None):  
        return cls.from_buffer_copy(socket_buffer)  
  
    def __init__(self, socket_buffer=None):  
        pass
```

struct:
```python
import ipaddress  
import struct  
  
  
class IP:  
    def __init__(self, buff=None):  
        header = struct.unpack("<BBHHHI", buff)  
        self.type = header[0]  
        self.code = header[1]  
        self.control_sum = header[2]  
        self.id = header[3]  
        self.number = header[4]  
        self.additional_inf = header[5]
```

![[Pasted image 20250603224925.png]]
