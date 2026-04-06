
def fibonacci(limite=None):
    """
    Generador de la secuencia de Fibonacci.

    Si se proporciona un límite, genera números hasta ese valor.
    Si no, genera una secuencia infinita.

    Args:
        limite (int, opcional): valor máximo de la secuencia

    Yields:
        int: siguiente número de Fibonacci
    """
    a, b = 0, 1

    while True:
        if limite is not None and a > limite:
            break

        yield a
        a, b = b, a + b


if __name__ == "__main__":
    # 🔹 Primeros 10 valores (infinito controlado)
    fib = fibonacci()

    print("Primeros 10 números:")
    for _ in range(10):
        print(next(fib), end=", ")
    print("\n")

    # 🔹 Con límite
    print("Fibonacci hasta 100:")
    for n in fibonacci(limite=100):
        print(n, end=", ")
    print()