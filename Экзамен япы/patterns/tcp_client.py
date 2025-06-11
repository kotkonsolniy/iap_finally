import socket

target_host = '127.0.0.1'
#target_host = 'sp-sys.ru'
target_port = 13377
#target_port = 80

# создаем обьект сокета
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# подключаем клиент
client.connect((target_host, target_port))

# отправляем данные

# client.send(b'GET / HTTP/1.1\r\nHost: sp-sys.ru \r\n\r\n')  # \r\n обязательно!
client.send(b'BMSTU')


# принимаем данные

response = client.recv(5096)  # 5096 - сколько байтов принимают, обычно ставят while true
print(response.decode())
client.close()
