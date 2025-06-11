import socket
import argparse
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [UDP CLIENT] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler("udp_client.log"),
        logging.StreamHandler()
    ]
)


def start_udp_client(host: str, port: int, message: str):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(message.encode(), (host, port))
        logging.info(f"Отправлено сообщение на {host}:{port}")

        data, _ = s.recvfrom(1024)
        logging.info(f"Ответ от сервера: {data.decode()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UDP-клиент")
    parser.add_argument("--host", default="127.0.0.1", help="IP адрес сервера")
    parser.add_argument("--port", type=int, default=9999, help="Порт сервера")
    parser.add_argument("--message", default="Привет, UDP-сервер!", help="Сообщение для отправки")
    args = parser.parse_args()

    start_udp_client(args.host, args.port, args.message)
