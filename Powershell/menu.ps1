<#
.SYNOPSIS
Menu de ciberseguridad en PowerShell

.DESCRIPTION
Este script permite:
1. Enviar archivos a VirusTotal.
2. Calcular hashes y consultarlos en VirusTotal.
3. Analizar procesos activos en base a su hash.

.NOTES
Requiere una clave Valida de API para VirusTotal.
#>

Set-StrictMode -Version Latest

$global:api = Read-Host "Ingresa tu API Key de VirusTotal"
$global:headers = @{ "x-apikey" = $global:api }

Import-Module -Name "$PSScriptRoot\escaneo.psm1"
Import-Module -Name "$PSScriptRoot\hashes.psm1"
Import-Module -Name "$PSScriptRoot\procesos_maliciosos.psm1"

while ($true) {
    Clear-Host
    Write-Host "=====MENU=====" -ForegroundColor Green
    Write-Host "1. Escaneo de archivos" -ForegroundColor Yellow
    Write-Host "2. Analizar Hashes " -ForegroundColor White    
    Write-Host "3. Verificar los hashes de los procesos activos y consultarlos con Virustotal" -ForegroundColor Blue
    Write-Host "4. Salir" -ForegroundColor Magenta
    Write-Host "================" -ForegroundColor Green
    $opcion_escogida = Read-Host "Seleccione una opcion"  

    switch ($opcion_escogida) {
        1 {
            Write-Host "El archivo no puede pesar mas de 30MB" -ForegroundColor Red
            Write-Host "El escaneo tomara 60 segundos" -ForegroundColor Yellow
            $ruta= Read-Host "Ingrese la ruta del archivo"
            escaneo -ruta_archivo $ruta
            Pause
        }
        2 {
            $ruta = Read-Host "Ingrese la ruta del archivo"
            analizar_hash -ruta_archivo $ruta
            Pause
        }
        3 {
            Write-Host "El escaneo esta empezando" -ForegroundColor Yellow
            Write-Host "=============INICIO=============" -ForegroundColor Green
            procesos_maliciosos
            Write-Host "=============FINAL=============" -ForegroundColor Green
            Pause
        }
        4 {
            Write-Host "Saliendo" -ForegroundColor Yellow
            break
        }
    }
}
