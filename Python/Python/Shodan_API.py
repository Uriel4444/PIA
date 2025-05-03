import shodan
import time


#Enter your api key inside the quotes
API_KEY = ''
api = shodan.Shodan(API_KEY)

def crear_alerta(nombre, red):
    try:
        alerta = api.create_alert(nombre, [red])
        print(f'Alerta creada: {alerta}')
    except shodan.APIError as e:
        print(f'Error al crear la alerta: {e}')

def eliminar_alerta(alerta_id):
    try:
        api.delete_alert(alerta_id)
        print(f'Alerta {alerta_id} eliminada.')
    except shodan.APIError as e:
        print(f'No existe la alerta: {e}')

def listar_alertas():
    try:
        alertas = api.alerts()
        if alertas:
            print('Alertas actuales:')
            for alerta in alertas:
                print(f"ID: {alerta['id']} - Nombre: {alerta['name']} - Red: {alerta['filters']['ip']}")
        else:
            print('No hay alertas activas.')
    except shodan.APIError as e:
        print(f'Error al listar las alertas: {e}')

def monitorizar_red():
    try:
        alertas = api.alerts()
        for alerta in alertas:
            print(f'Alerta: {alerta["name"]}, ID: {alerta["id"]}')
            triggers = api.alert_triggers()
            for trigger in triggers:
                print(f'Trigger: {trigger["rule"]}, Descripción: {trigger["description"]}')
    except shodan.APIError as e:
                print(f'Error al monitorear las alertas: {e}')

def menu():
    while True:
        print("\n--- Menú de Alertas Shodan ---")
        print("1. Generar nueva alerta")
        print("2. Eliminar alerta")
        print("3. Listar alertas")
        print("4. Monitorear red por alertas")
        print("5. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            nombre = input("Introduce el nombre de la alerta: ")
            red = input("Introduce la red o IP (ejemplo, '192.168.1.0/24'): ")
            crear_alerta(nombre, red)
        elif opcion == '2':
            alerta_id = input("Introduce el ID de la alerta para eliminar: ")
            eliminar_alerta(alerta_id)
        elif opcion == '3':
            listar_alertas()
        elif opcion == '4':
            monitorizar_red()
        elif opcion == '5':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida, intenta de nuevo.")

if __name__ == '__main__':
    menu()

