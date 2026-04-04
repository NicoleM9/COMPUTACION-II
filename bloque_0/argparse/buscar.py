import argparse
import sys


def buscar_en_archivo(f, nombre, args, mostrar_nombre):
    coincidencias = 0

    for num_linea, linea in enumerate(f, 1):
        linea_original = linea.rstrip("\n")

        texto = linea_original
        patron = args.patron

        if args.ignore_case:
            texto = texto.lower()
            patron = patron.lower()

        coincide = patron in texto

        if args.invert:
            coincide = not coincide

        if coincide:
            coincidencias += 1

            if not args.count:
                salida = ""

                if mostrar_nombre:
                    salida += f"{nombre}:"

                if args.line_number:
                    salida += f"{num_linea}:"

                salida += linea_original

                print(salida)

    return coincidencias


def main():
    parser = argparse.ArgumentParser(description="Mini grep en Python")

    parser.add_argument("patron", help="Patrón a buscar")
    parser.add_argument("archivos", nargs="*", help="Archivos a procesar")

    parser.add_argument("-i", "--ignore-case", action="store_true",
                        help="Ignorar mayúsculas/minúsculas")
    parser.add_argument("-n", "--line-number", action="store_true",
                        help="Mostrar número de línea")
    parser.add_argument("-c", "--count", action="store_true",
                        help="Mostrar solo cantidad de coincidencias")
    parser.add_argument("-v", "--invert", action="store_true",
                        help="Invertir la búsqueda")

    args = parser.parse_args()

    total = 0

    # 📌 Caso stdin (pipe)
    if not args.archivos:
        if not sys.stdin.isatty():
            coincidencias = buscar_en_archivo(
                sys.stdin,
                "",
                args,
                mostrar_nombre=False
            )
            if args.count:
                print(coincidencias)
            sys.exit(0)
        else:
            print("Error: Debés especificar archivos o usar stdin.")
            sys.exit(1)

    # 📌 Caso archivos
    multiples = len(args.archivos) > 1

    for nombre in args.archivos:
        try:
            with open(nombre, "r", encoding="utf-8") as f:
                coincidencias = buscar_en_archivo(
                    f,
                    nombre,
                    args,
                    mostrar_nombre=multiples
                )

                total += coincidencias

                if args.count:
                    if multiples:
                        print(f"{nombre}: {coincidencias} coincidencias")
                    else:
                        print(f"{coincidencias} coincidencias")

        except FileNotFoundError:
            print(f"Error: no se pudo abrir {nombre}")

    if args.count and multiples:
        print(f"Total: {total} coincidencias")


if __name__ == "__main__":
    main()