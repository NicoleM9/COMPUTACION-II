#!/usr/bin/env python3

import os
import argparse
import hashlib
from datetime import datetime


# -------------------------
# Obtener archivos
# -------------------------
def get_files(path, recursive=False):
    files = {}

    if recursive:
        for root, _, filenames in os.walk(path):
            for name in filenames:
                full = os.path.join(root, name)
                rel = os.path.relpath(full, path)
                try:
                    files[rel] = os.stat(full)
                except (PermissionError, FileNotFoundError):
                    continue
    else:
        for name in os.listdir(path):
            full = os.path.join(path, name)
            if os.path.isfile(full):
                try:
                    files[name] = os.stat(full)
                except (PermissionError, FileNotFoundError):
                    continue

    return files


# -------------------------
# Hash SHA256
# -------------------------
def file_hash(path):
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while chunk := f.read(4096):
                h.update(chunk)
    except:
        return None
    return h.hexdigest()


# -------------------------
# MAIN
# -------------------------
def main():
    parser = argparse.ArgumentParser(description="Comparador de directorios")

    parser.add_argument("dir1")
    parser.add_argument("dir2")
    parser.add_argument("--recursive", action="store_true")
    parser.add_argument("--checksum", action="store_true")

    args = parser.parse_args()

    files1 = get_files(args.dir1, args.recursive)
    files2 = get_files(args.dir2, args.recursive)

    set1 = set(files1.keys())
    set2 = set(files2.keys())

    only1 = set1 - set2
    only2 = set2 - set1
    common = set1 & set2

    print(f"Comparando {args.dir1} con {args.dir2}...\n")

    # -------------------------
    # Solo en dir1
    # -------------------------
    print(f"Solo en {args.dir1}:")
    for f in sorted(only1):
        print(" ", f)

    print(f"\nSolo en {args.dir2}:")
    for f in sorted(only2):
        print(" ", f)

    # -------------------------
    # Comparaciones
    # -------------------------
    modified_size = []
    modified_time = []
    modified_content = []
    identical = 0

    for f in common:
        f1 = os.path.join(args.dir1, f)
        f2 = os.path.join(args.dir2, f)

        s1 = files1[f]
        s2 = files2[f]

        if args.checksum:
            h1 = file_hash(f1)
            h2 = file_hash(f2)

            if h1 != h2:
                modified_content.append(f)
            else:
                identical += 1

        else:
            if s1.st_size != s2.st_size:
                modified_size.append((f, s1.st_size, s2.st_size))

            elif int(s1.st_mtime) != int(s2.st_mtime):
                modified_time.append((f, s1.st_mtime, s2.st_mtime))

            else:
                identical += 1

    # -------------------------
    # Mostrar resultados
    # -------------------------
    if args.checksum:
        if modified_content:
            print("\nModificados (contenido diferente):")
            for f in modified_content:
                print(f"  {f}")
    else:
        if modified_size:
            print("\nModificados (tamaño diferente):")
            for f, s1, s2 in modified_size:
                print(f"  {f} ({s1} -> {s2} bytes)")

        if modified_time:
            print("\nModificados (fecha diferente):")
            for f, t1, t2 in modified_time:
                d1 = datetime.fromtimestamp(t1).strftime("%Y-%m-%d")
                d2 = datetime.fromtimestamp(t2).strftime("%Y-%m-%d")
                print(f"  {f} ({d1} -> {d2})")

    print(f"\nIdénticos: {identical} archivos")


# -------------------------
if __name__ == "__main__":
    main()
