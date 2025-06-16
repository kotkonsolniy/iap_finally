# multithreading_example.py
import threading
import time

def task(name, delay):
    print(f"[{name}] started")
    time.sleep(delay)
    print(f"[{name}] finished after {delay} seconds")

# Создаем потоки
thread1 = threading.Thread(target=task, args=("Thread 1", 3))
thread2 = threading.Thread(target=task, args=("Thread 2", 2))

# Запускаем потоки
thread1.start()
thread2.start()

# Ждем завершения потоков
thread1.join()
thread2.join()

print("Main thread finished")
