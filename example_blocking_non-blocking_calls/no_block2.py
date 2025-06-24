import asyncio

async def download_data(name, seconds):
    print(f"{name}: Начинаем загрузку...")
    await asyncio.sleep(seconds)  # неблокирующий вызов
    print(f"{name}: Загрузка завершена через {seconds} сек")

async def main():
    # запускаем обе задачи одновременно
    await asyncio.gather(
        download_data("Файл 1", 3),
        download_data("Файл 2", 2)
    )

asyncio.run(main())
