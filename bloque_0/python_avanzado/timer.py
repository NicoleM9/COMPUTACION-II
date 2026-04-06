
import time
from typing import Optional
from contextlib import contextmanager


class Timer:
    """
    Context manager para medir el tiempo de ejecución de un bloque de código.

    Permite:
    - nombre opcional
    - acceso a elapsed durante y después del bloque
    - impresión automática al salir si se proporciona nombre
    """

    def __init__(self, nombre: Optional[str] = None):
        self.nombre = nombre
        self._start = None
        self._end = None

    def __enter__(self):
        self._start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._end = time.perf_counter()

        if self.nombre:
            print(f"[Timer] {self.nombre}: {self.elapsed:.3f}s")

        return False  # no suprime excepciones

    @property
    def elapsed(self) -> float:
        """
        Devuelve el tiempo transcurrido en segundos.
        Funciona tanto dentro como fuera del bloque.
        """
        if self._start is None:
            return 0.0

        end = self._end if self._end is not None else time.perf_counter()
        return end - self._start


@contextmanager
def timer(nombre: Optional[str] = None):
    """
    Versión alternativa de Timer usando contextmanager.
    """
    start = time.perf_counter()
    end = None

    class TimerObj:
        @property
        def elapsed(self):
            current_end = end if end is not None else time.perf_counter()
            return current_end - start

    t = TimerObj()

    try:
        yield t
    finally:
        end = time.perf_counter()
        if nombre:
            print(f"[Timer] {nombre}: {t.elapsed:.3f}s")


if __name__ == "__main__":
    # 🔹 Uso con clase (con nombre)
    with Timer("Procesamiento"):
        datos = [x**2 for x in range(1_000_000)]

    # 🔹 Uso sin nombre
    with Timer() as t:
        time.sleep(0.5)
    print(f"El bloque tardó {t.elapsed:.3f} segundos")

    # 🔹 Acceso durante ejecución
    with Timer() as t:
        time.sleep(0.3)
        print(f"Después del paso 1: {t.elapsed:.3f}s")
        time.sleep(0.3)
        print(f"Después del paso 2: {t.elapsed:.3f}s")

    # 🔹 Uso con contextmanager
    with timer("Bloque alternativo"):
        time.sleep(0.4)