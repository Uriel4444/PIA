#!/bin/bash

function menu(){
	echo "Monitoreo de Red"
	echo "1.- Ver trafico en tiempo real"
	echo "2.- Ver Conexiones Activas"
	echo "3.- Ver uso de ancho de bando"
	echo "4.- Generar reporte"
	echo "5.- Salir..."
	echo "Seleccione una opcion: "
}

if [ "$EUID" -ne 0 ]; then
	echo "Debe de ejecutar el script como root..."
	exit 1
fi

for cmd in iftop ss vnstat; do
	if ! command -v $cmd &> /dev/null; then
		echo "Error... El comando '$cmd' no esta instalado"
		echo "Puede instalar el comando con: sudo apt install $cmd"
		exit 1
	fi
done

INTERFAZ=${1:-$(ip route | grep default | awk '{print $5}' | head -n1)}

while true; do
	menu
	read -r opc

	case $opc in
	1)
		echo "Mostrando trafico en tiempo real para la interfaz $INTERFAZ (Crtl+C para salir)"
		iftop -i "$INTERFAZ"
		;;
	2)
		echo "Mostrando conexiones arctivas..."
		ss -tunap
		;;
	3)
		echo "Mostrando uso de ancho de banda (Crtl+C para salir)"
		vnstat -l -i "$INTERFAZ"
		;;
	4)
		REPORTE="reporte_red_$(date +%Y%m%d_%H%M%S).txt"
		echo "Generando reporte de red en $REPORTE"
		{
			echo "Reporte de Monitoreo de Red"
			echo "Fecha: $(date)"
			echo ""
			echo "--- Conexiones Activas ---"
			ss -tunap
			echo ""
			echo "--- Ancho de Banda -------"
			vnstat -i "$INTERFAZ"
		} > "$REPORTE"
		echo "Reporte generado exitosamente: $REPORTE"
		;;
	5)
		echo "Saliendo..."
		exit 0
		;;
	*)
		echo "Opcion no valida, intente de nuevo"
		;;
	esac
done

