
#!/usr/bin/env python3
"""extraer_ips_de_log.py
----------------------------------------
Lee un archivo de log generado con:

    netstat -n > conexiones.log     (Windows/PowerShell)
    netstat -n > conexiones.log     (Linux/Bash)

Extrae todas las direcciones IPv4 que encuentre y las
guarda, una por línea, en 'ips.txt'.  También soporta
logs guardados en UTF‑16 (caso típico de PowerShell)
y en UTF‑8 (caso típico de Bash).

Uso desde terminal:
    python extraer_ips_de_log.py --log conexiones.log
Opciones:
    --log   Ruta del archivo log de entrada   (obligatorio)
    --out   Nombre del archivo de salida      (opcional, por defecto ips.txt)
----------------------------------------"""

import argparse
import re
import pathlib
import platform
import sys

# Expresión regular para IPv4: 0.0.0.0 – 255.255.255.255
IP_RE = re.compile(r'(?:\d{1,3}\.){3}\d{1,3}')

def main():
    # --- Definición de argumentos ---
    parser = argparse.ArgumentParser(
        description="Extrae IPs de un log netstat")
    parser.add_argument(
        "--log", required=True, help="Archivo de log de entrada")
    parser.add_argument(
        "--out", default="ips.txt", help="Archivo de salida (una IP por línea)")
    args = parser.parse_args()

    # --- Verificación rápida de sistema operativo ---
    if platform.system().lower() not in ("windows", "linux"):
        sys.exit("SO no soportado")

    # --- Lectura del archivo (primero UTF‑16, luego UTF‑8) ---
    log_path = pathlib.Path(args.log)
    try:
        texto = log_path.read_text(encoding="utf-16", errors="ignore")
    except UnicodeError:
        texto = log_path.read_text(encoding="utf-8", errors="ignore")

    # --- Búsqueda y deduplicación de IPs ---
    ips = sorted(set(IP_RE.findall(texto)))

    # --- Escritura del resultado ---
    out_path = pathlib.Path(args.out)
    out_path.write_text("\n".join(ips))

    print(f"[+] {len(ips)} IPs extraídas → {out_path.resolve()}")
    
if __name__ == "__main__":
    main()
