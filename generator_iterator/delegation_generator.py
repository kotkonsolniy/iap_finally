def count_up_to(n):
    for i in range(1, n + 1):
        yield i


def delegating_generator():
    # Делегируем генерацию count_up_to(5)
    yield from count_up_to(5)

    # После завершения делегирования продолжаем свою логику
    yield "Дальше свои значения"
    yield "Ещё одно значение"


# Используем delegating_generator()
gen = delegating_generator()
for value in gen:
    print(value)