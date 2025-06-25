import threading
import time
import logging
from concurrent.futures import ThreadPoolExecutor
import requests

# Создаём логгер
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Формат логов
log_format = logging.Formatter("%(asctime)s [%(levelname)s] [%(threadName)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# Обработчик для файла
file_handler = logging.FileHandler("log.txt", encoding="utf-8")
file_handler.setFormatter(log_format)
logger.addHandler(file_handler)

# (опционально) обработчик для консоли
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)
thread_local = threading.local()  # Локальное хранилище для каждого потока

def main():
    sites = [
        "https://www.yandex.ru",
        "https://bmstu.ru",
    ] * 800  # Умножаем список сайтов для большей нагрузки

    logging.info("Начало загрузки сайтов")
    start_time = time.perf_counter()

    download_all_sites(sites)

    duration = time.perf_counter() - start_time
    logging.info(f"Завершено: загружено {len(sites)} сайтов за {duration:.2f} секунд")

def download_all_sites(sites):
    max_threads = 5
    logging.info(f"Запуск ThreadPoolExecutor с {max_threads} потоками")
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        executor.map(download_site, sites)

def download_site(url):
    try:
        session = get_session_for_thread()
        with session.get(url, timeout=5) as response:
            logging.info(f"Загружено {len(response.content)} байт с {url}")
    except requests.RequestException as e:
        logging.error(f"Ошибка при загрузке {url}: {e}")

def get_session_for_thread():
    if not hasattr(thread_local, "session"):
        logging.debug("Создание новой сессии для потока")
        thread_local.session = requests.Session()
    return thread_local.session

if __name__ == "__main__":
    main()
