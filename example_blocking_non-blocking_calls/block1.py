import time

def download_data(name, seconds):
    print(f"{name}: Начинаем загрузку...")
    time.sleep(seconds)  # блокирующий вызов
    print(f"{name}: Загрузка завершена через {seconds} сек")

def main():
    download_data("Файл 1", 3)
    download_data("Файл 2", 2)

main()
