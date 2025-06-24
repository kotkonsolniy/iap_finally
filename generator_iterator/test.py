def count(n):
    for i in range(1, n+1):
        yield i
gen = count(5)
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
