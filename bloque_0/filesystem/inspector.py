#!/usr/bin/env python3

import os
import sys
import stat
import pwd
import grp
from datetime import datetime

def human_size(size):
    for unit in ['B','KB','MB','GB','TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

def get_file_type(mode):
    if stat.S_ISREG(mode):
        return "archivo regular"
    elif stat.S_ISDIR(mode):
        return "directorio"
    elif stat.S_ISLNK(mode):
        return "enlace simbólico"
    elif stat.S_ISCHR(mode):
        return "dispositivo de caracteres"
    elif stat.S_ISBLK(mode):
        return "dispositivo de bloques"
    elif stat.S_ISFIFO(mode):
        return "FIFO/pipe"
    elif stat.S_ISSOCK(mode):
        return "socket"
    else:
        return "desconocido"

def format_permissions(mode):
    return stat.filemode(mode), format(mode & 0o777, '03o')

def format_time(ts):
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

def main():
    if len(sys.argv) != 2:
        print("Uso: python inspector.py <ruta>")
        sys.exit(1)

    path = sys.argv[1]

    try:
        st = os.lstat(path)  # importante para symlinks
    except FileNotFoundError:
        print("Error: el archivo no existe")
        sys.exit(1)
    except PermissionError:
        print("Error: permisos insuficientes")
        sys.exit(1)

    file_type = get_file_type(st.st_mode)
    perms_str, perms_oct = format_permissions(st.st_mode)

    try:
        owner = pwd.getpwuid(st.st_uid).pw_name
    except KeyError:
        owner = str(st.st_uid)

    try:
        group = grp.getgrgid(st.st_gid).gr_name
    except KeyError:
        group = str(st.st_gid)

    print(f"Archivo: {path}")
    print(f"Tipo: {file_type}")

    if file_type == "enlace simbólico":
        try:
            target = os.readlink(path)
            print(f"-> Apunta a: {target}")
        except OSError:
            print("-> Enlace roto")

    print(f"Tamaño: {st.st_size} bytes ({human_size(st.st_size)})")
    print(f"Permisos: {perms_str} ({perms_oct})")
    print(f"Propietario: {owner} (uid: {st.st_uid})")
    print(f"Grupo: {group} (gid: {st.st_gid})")
    print(f"Inodo: {st.st_ino}")
    print(f"Enlaces duros: {st.st_nlink}")
    print(f"Creación: {format_time(st.st_ctime)}")
    print(f"Última modificación: {format_time(st.st_mtime)}")
    print(f"Último acceso: {format_time(st.st_atime)}")

    if stat.S_ISDIR(st.st_mode):
        try:
            count = len(os.listdir(path))
            print(f"Contenido: {count} elementos")
        except PermissionError:
            print("Contenido: acceso denegado")

if __name__ == "__main__":
    main()
