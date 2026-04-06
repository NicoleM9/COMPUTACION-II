
from functools import wraps
import time
from typing import Tuple, Type


def retry(max_attempts: int = 3, delay: float = 1, exceptions: Tuple[Type[BaseException], ...] = (Exception,)):
    """
    Decorador que reintenta la ejecución de una función si ocurre una excepción.

    Args:
        max_attempts: número máximo de intentos
        delay: tiempo de espera entre intentos (en segundos)
        exceptions: tupla de excepciones a capturar
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for intento in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)

                except exceptions as e:
                    # Último intento → relanzar excepción
                    if intento == max_attempts:
                        print(f"Intento {intento}/{max_attempts} falló: {e}")
                        raise

                    # Intento intermedio
                    print(f"Intento {intento}/{max_attempts} falló: {e}. Esperando {delay}s...")
                    time.sleep(delay)

        return wrapper

    return decorator

if __name__ == "__main__":
    import random

    @retry(max_attempts=3, delay=1)
    def conectar_servidor():
        if random.random() < 0.7:
            raise ConnectionError("Servidor no disponible")
        return "Conectado exitosamente"

    try:
        resultado = conectar_servidor()
        print(resultado)
    except ConnectionError:
        print("Falló después de 3 intentos")