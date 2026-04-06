import os

class archivo_temporal:

    def __init__(self, nombre):
        self.nombre = nombre
        self._archivo = None

    def __enter__(self):
        self._archivo = open(self.nombre, "w+")
        return self._archivo

    def __exit__(self, exc_type, exc_value, traceback):
        if self._archivo and not self._archivo.closed:
            self._archivo.close()

        if os.path.exists(self.nombre):
            os.remove(self.nombre)

        return False


if __name__ == "__main__":
    with archivo_temporal("test.txt") as f:
        f.write("Datos de prueba\n")
        f.seek(0)
        print(f.read())

    print("¿Existe el archivo?", os.path.exists("test.txt"))