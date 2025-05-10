
#!/usr/bin/env python3
"""ips_malos.py
----------------------------------------
Toma dos archivos:
    1) ips.txt        → Lista de IPs a revisar (salida de extraer_ips_de_log.py)
    2) ips_malos.txt  → Tu 'lista negra' (una IP por línea)

Para cada IP indica si está en la lista negra y guarda
los resultados en un CSV: ips_maliciosos.csv

Uso:
    python ips_malos.py --ips ips.txt --bad ips_malos.txt
----------------------------------------"""

import argparse
import csv
import hashlib
import datetime
import pathlib
import platform
import sys

def sha256(path: pathlib.Path) -> str:
    """Calcula el SHA‑256 del archivo dado"""
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()

def main():
    # --- Argumentos de entrada ---
    parser = argparse.ArgumentParser(
        description="Compara IPs contra lista negra")
    parser.add_argument("--ips", default="ips.txt", help="Archivo con IPs a revisar")
    parser.add_argument("--bad", default="ips_malos.txt", help="Lista negra")
    parser.add_argument("--out", default="ips_maliciosos.csv", help="CSV de salida")
    args = parser.parse_args()

    # --- Check SO ---
    if platform.system().lower() not in ("windows", "linux"):
        sys.exit("SO no soportado")

    # --- Carga de archivos ---
    ips_file = pathlib.Path(args.ips)
    if not ips_file.exists():
        sys.exit("No existe ips.txt; corre primero extraer_ips_de_log.py")

    ips   = ips_file.read_text().splitlines()
    malos = set(pathlib.Path(args.bad).read_text().splitlines())             if pathlib.Path(args.bad).exists() else set()

    # --- Generación del CSV ---
    out_path = pathlib.Path(args.out)
    with out_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["IP", "Es_maliciosa"])
        for ip in ips:
            w.writerow([ip, "SI" if ip in malos else "NO"])

    # --- Resumen en consola ---
    print("CSV listo :", out_path.resolve())
    print("SHA-256   :", sha256(out_path))
    print("Fecha     :", datetime.datetime.now().isoformat())

if __name__ == "__main__":
    main()
