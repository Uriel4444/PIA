#!/usr/bin/python
from pathlib import Path 
import logger
import logging
from logger import init_logger

import metadata
import ip_abuse_checker
import tcpdump
import Shodan_API

current_directory = Path.cwd()
print("Current Working Directory:", current_directory)
logger = init_logger('my_log_file.log', logging.INFO)

def perform_task():
    logger.info("Starting the task...")
    try:
       
            while True:
                print("\n--- Menu principal ---")
                print("1. Extraer metadatos de una imagen")
                print("2. Verificar direccion IP con AbuseIPDB")
                print("3. Monitorear trafico de red")
                print("4. Administrar alertas de Shodan")
                print("5. Salir")

                choice = input("Selecciona una opcion (1-5): ")

                if choice == '1':
                    image_path = input("Ingresa la ruta de la imagen: ")
                    metadata.get_metadata(image_path)
                    logger.debug()

                elif choice == '2':
                    ip_abuse_checker.main()
                    logger.debug()

                elif choice == '3':
                    tcpdump.redirect()
                    logger.debug()

                elif choice == '4':
                    Shodan_API.menu()
                    logger.debug()

                elif choice == '5':
                    print("Saliendo del programa")
                    break

                else:
                    print("Opcion invalida, por favor selecciona una opcion del 1 al 5.")
       

    except ZeroDivisionError:
        logger.error(" a selection of options is incorrect", exc_info=True)
    
    logger.info("Task completed.")


def main():
    logger.info("Application started.")

    perform_task()
    logger.error("Application has finished")

if __name__ == "__main__":
    main()
