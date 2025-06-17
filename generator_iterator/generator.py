def counter(start, end):
    while start <= end:
        yield start
        start += 1

# Использование:
for num in counter(1, 5):
    print(num)
