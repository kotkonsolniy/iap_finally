# non_blocking_example.py
import asyncio

async def task1():
    print("Task 1 started")
    await asyncio.sleep(3)  # неблокирующий вызов
    print("Task 1 finished")

async def task2():
    print("Task 2 started")
    print("Task 2 finished")

async def main():
    await asyncio.gather(task1(), task2())

asyncio.run(main())
