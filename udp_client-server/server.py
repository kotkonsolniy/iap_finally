import socket
import argparse
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [UDP SERVER] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler("udp_server.log"),
        logging.StreamHandler()
    ]
)


def start_udp_server(host: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((host, port))
        logging.info(f"UDP сервер слушает {host}:{port}")

        while True:
            data, addr = s.recvfrom(1024)
            logging.info(f"Получено от {addr}: {data.decode()}")
            s.sendto(data, addr)  # Эхо-ответ


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UDP-сервер")
    parser.add_argument("--host", default="127.0.0.1", help="IP адрес сервера")
    parser.add_argument("--port", type=int, default=9999, help="Порт сервера")
    args = parser.parse_args()

    start_udp_server(args.host, args.port)
