from functools import wraps
from datetime import datetime


def log_llamada(func):
    """
    Decorador que registra cada llamada a una función,
    mostrando timestamp, argumentos y valor de retorno.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Formatear argumentos
        args_str = ", ".join(repr(a) for a in args)
        kwargs_str = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
        params = ", ".join(filter(None, [args_str, kwargs_str]))

        print(f"[{timestamp}] Llamando a {func.__name__}({params})")

        resultado = func(*args, **kwargs)

        print(f"[{timestamp}] {func.__name__} retornó {resultado!r}")

        return resultado

    return wrapper

if __name__ == "__main__":

    @log_llamada
    def sumar(a, b):
        return a + b

    @log_llamada
    def saludar(nombre, entusiasta=False):
        sufijo = "!" if entusiasta else "."
        return f"Hola, {nombre}{sufijo}"

    sumar(3, 5)
    saludar("Ana", entusiasta=True)
