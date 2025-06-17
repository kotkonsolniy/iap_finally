class Counter:
    def __init__(self, start, end):
        self.current = start
        self.end = end

    def __iter__(self):
        return self  # Итератор сам себя возвращает

    def __next__(self):
        if self.current > self.end:
            raise StopIteration
        else:
            value = self.current
            self.current += 1
            return value

# Использование:
for num in Counter(1, 5):
    print(num)
