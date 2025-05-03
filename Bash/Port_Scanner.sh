#!/bin/bash

function scan() {
	read -p "Ingrese la IP o dominio a escanear: " obj
	read -p "Ingresa el rango de puertos (ej: 20,80,443): " puertos

	if [[ -z "$obj" || -z "$puertos" ]]; then
		echo "Error: Debes ingresar una IP y al menos un puerto"
		return
	fi

	IFS=',' read -ra PORT_ARRAY <<< "$puertos"
	REPORTE="reporte_escaneo_$(date +%Y%m%d_%H%M%S).txt"

	echo "Escaneando los puertos [$puertos] en $obj"
	echo "------- REPORTE DE ESCANEO DE PUERTOS -------" > "$REPORTE"
	echo "Fecha: $(date)" >> "$REPORTE"
	echo "Objetivo: $obj" >> "$REPORTE"
	echo "Puertos: $puertos" >> "$REPORTE"
	echo "" >> "$REPORTE"

	for port in "${PORT_ARRAY[@]}"; do
		if [[ "$port" =~ ^[0-9]+$ ]]; then
			timeout 1 bash -c "echo > /dev/tcp/$obj/$port" 2>/dev/null &&
			{ echo "Puerto $port está Abierto"; echo "Puerto $port: Abierto" >> "$REPORTE" ; } ||
			{ echo "Puerto $port está Cerrado"; echo "Puerto $port: Cerrado" >> "$REPORTE" ; }
		else
			echo "Puerto invalido: '$port' (omitido)"
			echo "Puerto invalido: '$port' (omitido)" >> "$REPORTE"
		fi
	done

	echo ""
	echo "Reporte guardado en: $REPORTE"
}

function menu() {
	echo "Menu principal - Escaneo de puertos"
	echo "1.- Escanear puertos"
	echo "2.- Salir"
	read -p "Opción: " op

	case $op in
		1) scan ;;
		2) exit 0 ;;
		*) echo "Opción no válida" ;;
	esac
}

while true; do
	menu
done

