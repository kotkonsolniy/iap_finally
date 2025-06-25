import asyncio
import time
import aiohttp
import logging

# Настройка логирования
logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Лог в файл
file_handler = logging.FileHandler("async_download.log", encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Лог в консоль
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


async def main():
    sites = [
        "https://www.yandex.ru",
        "https://bmstu.ru",
    ] * 800
    start_time = time.perf_counter()
    await download_all_sites(sites)
    duration = time.perf_counter() - start_time
    logger.info(f"Downloaded {len(sites)} sites in {duration:.2f} seconds")


async def download_all_sites(sites):
    async with aiohttp.ClientSession() as session:
        tasks = [download_site(url, session) for url in sites]
        await asyncio.gather(*tasks, return_exceptions=True)


async def download_site(url, session):
    try:
        async with session.get(url) as response:
            content = await response.read()
            logger.info(f"Read {len(content)} bytes from {url}")
    except Exception as e:
        logger.error(f"Error downloading {url}: {e}")


if __name__ == "__main__":
    asyncio.run(main())
