import socket
import argparse
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [SERVER] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler("server.log"),
        logging.StreamHandler()
    ]
)


def start_server(host: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        logging.info(f"Сервер слушает {host}:{port}")

        conn, addr = s.accept()
        with conn:
            logging.info(f"Подключено к {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                logging.info(f"Получено: {data.decode()}")
                conn.sendall(data)  # Эхо-ответ


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP-сервер")
    parser.add_argument("--host", default="127.0.0.1", help="IP адрес сервера")
    parser.add_argument("--port", type=int, default=65432, help="Порт сервера")
    args = parser.parse_args()

    start_server(args.host, args.port)
