import atexit
import time
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import requests
import logging

# === Настройка логирования ===
logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] [%(processName)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Логи в файл
file_handler = logging.FileHandler("process_pool.log", encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Логи в консоль
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

session = None  # Глобальная сессия, инициализируется в init_process


def main():
    sites = [
        "https://www.yandex.ru",
        "https://bmstu.ru"
    ] * 800
    start_time = time.perf_counter()
    download_all_sites(sites)
    duration = time.perf_counter() - start_time
    logger.info(f'Downloaded {len(sites)} sites in {duration:.2f} seconds')


def download_all_sites(sites):
    with ProcessPoolExecutor(initializer=init_process) as executor:
        executor.map(download_site, sites)


def download_site(url):
    try:
        with session.get(url, timeout=5) as response:
            logger.info(f'Read {len(response.content)} bytes from {url}')
    except requests.RequestException as e:
        logger.error(f'Error downloading {url}: {e}')


def init_process():
    global session
    session = requests.Session()
    atexit.register(session.close)
    logger.info(f"Initialized session in process {multiprocessing.current_process().name}")


if __name__ == '__main__':
    main()
