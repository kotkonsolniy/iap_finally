import threading

x = 0

def add():
    global x
    for _ in range(1000000):
        x += 1

t1 = threading.Thread(target=add)
t2 = threading.Thread(target=add)

t1.start()
t2.start()
t1.join()
t2.join()

print(x)
