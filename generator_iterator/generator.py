def counter(start, end):
    while start <= end:
        yield start
        start += 1

# делегирование генераторов
for num in counter(1, 5):
    print(num)

def subgenerator():
    yield 1
    yield 2
    yield 3

def delegating_generator():
    yield 0
    yield from subgenerator()  # делегирование
    yield 4

for val in delegating_generator():
    print(val)
