import argparse
import random
import string
import sys


def generar_password(longitud, usar_letras, usar_numeros, usar_simbolos):
    caracteres = ""

    if usar_letras:
        caracteres += string.ascii_letters
    if usar_numeros:
        caracteres += string.digits
    if usar_simbolos:
        caracteres += string.punctuation

    if not caracteres:
        print("Error: Debes seleccionar al menos un tipo de carácter.")
        sys.exit(1)

    password = "".join(random.choice(caracteres) for _ in range(longitud))
    return password


def main():
    parser = argparse.ArgumentParser(description="Generador de contraseñas seguras")

    parser.add_argument("longitud", type=int, help="Longitud de la contraseña")

    parser.add_argument("--numbers", action="store_true",
                        help="Incluir números")
    parser.add_argument("--symbols", action="store_true",
                        help="Incluir símbolos")
    parser.add_argument("--no-letters", action="store_true",
                        help="Excluir letras")

    args = parser.parse_args()

    usar_letras = not args.no_letters
    usar_numeros = args.numbers
    usar_simbolos = args.symbols

    password = generar_password(
        args.longitud,
        usar_letras,
        usar_numeros,
        usar_simbolos
    )

    print(password)


if __name__ == "__main__":
    main()
