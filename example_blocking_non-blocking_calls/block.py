# blocking_example.py
import time

def task1():
    print("Task 1 started")
    time.sleep(3)  # блокирующий вызов
    print("Task 1 finished")

def task2():
    print("Task 2 started")
    print("Task 2 finished")

task1()
task2()
