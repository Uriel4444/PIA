import argparse
import hashlib
import os
import platform
from datetime import datetime
import subprocess
import sys

def verificar_sistema():
    sistema = platform.system()
    print(f"Sistema operativo detectado: {sistema}")
    if sistema not in ['Windows', 'Linux']:
        raise SystemExit("Sistema no compatible. Solo se admite Windows o Linux.")

def ejecutar_comando(comando):
    try:
        resultado = subprocess.getoutput(comando)
        if resultado.strip() == "":
            raise RuntimeError(f"El comando '{comando}' no devolvió resultados.")
        return resultado
    except Exception as e:
        return f"Error ejecutando el comando '{comando}': {e}"

def ejecutar_tareas():
    try:
        # Tarea 1: Escaneo de puertos con Nmap (Python)
        salida_nmap = ejecutar_comando("nmap -sS 127.0.0.1")
        puertos_abiertos = [line for line in salida_nmap.splitlines() if "open" in line]

        # Tarea 2: Verificación de servicios en puertos abiertos (PowerShell)
        if platform.system() == "Windows":
            script_powershell = "Get-Service | Where-Object { $_.Status -eq 'Running' }"
            salida_powershell = ejecutar_comando(f"powershell -Command \"{script_powershell}\"")
        else:
            salida_powershell = "PowerShell no está disponible en Linux."

        # Tarea 3: Información de red (ipconfig/ifconfig)
        comando_red = "ipconfig" if platform.system() == "Windows" else "ifconfig"
        salida_red = ejecutar_comando(comando_red)

        return f"""
=== Escaneo Nmap ===
{salida_nmap}

=== Servicios en Puertos Abiertos (PowerShell) ===
{salida_powershell}

=== Información de Red ===
{salida_red}
"""
    except Exception as e:
        sys.exit(f"Error ejecutando tareas: {e}")

def generar_reporte(datos, formato, nombre_reporte):
    try:
        if formato == "txt":
            with open(nombre_reporte, "w") as file:
                file.write(datos)
        elif formato == "csv":
            import csv
            with open(nombre_reporte, "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Datos"])
                for line in datos.splitlines():
                    writer.writerow([line])
        elif formato == "html":
            with open(nombre_reporte, "w") as file:
                file.write(f"<html><body><pre>{datos}</pre></body></html>")
        elif formato == "xlsx":
            import pandas as pd
            df = pd.DataFrame({"Datos": datos.splitlines()})
            df.to_excel(nombre_reporte, index=False)
        else:
            raise ValueError("Formato de reporte no soportado.")
        return nombre_reporte
    except Exception as e:
        sys.exit(f"Error generando el reporte: {e}")

def calcular_hash_archivo(archivo):
    try:
        hash_md5 = hashlib.md5()
        with open(archivo, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except FileNotFoundError:
        sys.exit("El archivo del reporte no fue encontrado.")
    except Exception as e:
        sys.exit(f"Error calculando el hash del archivo: {e}")

def main():
    try:
        parser = argparse.ArgumentParser(description="Script de Ciberseguridad (Python + PowerShell)")
        parser.add_argument("--formato", required=True, choices=['txt', 'csv', 'html', 'xlsx'], help="Formato del reporte")
        parser.add_argument("--reporte", required=True, help="Nombre del archivo de reporte")

        args = parser.parse_args()

        verificar_sistema()
        datos = ejecutar_tareas()
        if not datos.strip():
            sys.exit("No se generaron datos en las tareas.")

        reporte = generar_reporte(datos, args.formato, args.reporte)
        if not os.path.exists(reporte):
            sys.exit("El reporte no fue creado correctamente.")

        hash_reporte = calcular_hash_archivo(reporte)
        print(f"Reporte generado: {reporte}")
        print(f"Hash del reporte: {hash_reporte}")
        print(f"Ubicación del reporte: {os.path.abspath(reporte)}")
        print(f"Fecha de ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    except KeyboardInterrupt:
        sys.exit("\nEjecución interrumpida por el usuario.")
    except Exception as e:
        sys.exit(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()