import socket
import argparse
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [CLIENT] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler("client.log"),
        logging.StreamHandler()
    ]
)

def start_client(host: str, port: int, message: str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        logging.info(f"Подключено к серверу {host}:{port}")
        s.sendall(message.encode())
        data = s.recv(1024)
        logging.info(f"Ответ от сервера: {data.decode()}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP-клиент")
    parser.add_argument("--host", default="127.0.0.1", help="IP адрес сервера")
    parser.add_argument("--port", type=int, default=65432, help="Порт сервера")
    parser.add_argument("--message", default="Привет, сервер!", help="Сообщение для отправки")
    args = parser.parse_args()

    start_client(args.host, args.port, args.message)
