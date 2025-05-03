function escaneo {
    param (
        [Parameter(Mandatory=$true)]
        [string]$ruta_archivo
    )

    $headers = $global:headers
    $url = "https://www.virustotal.com/api/v3/files"

    if (-not (Test-Path $ruta_archivo)) {
        Write-Host "El archivo no existe" -ForegroundColor Red
        return
    }

    if ((Get-Item $ruta_archivo).Length -gt 30MB) {
        Write-Host "El archivo no puede pesar mas de 30MB" -ForegroundColor Red
        return
    }

    $form = @{ file = Get-Item $ruta_archivo }

    try {
        $respuesta = Invoke-RestMethod -Uri $url -Method Post -Headers $headers -Form $form
        Start-Sleep -Seconds 60
        $analisis_id = $respuesta.data.id
        $resultado = Invoke-RestMethod -Uri "https://www.virustotal.com/api/v3/analyses/$analisis_id" -Headers $headers -Method Get
        Write-Host "============RESULTADO=============" -ForegroundColor Green
        $resultado.data.attributes.stats | Format-List
        Write-Host "===================================" -ForegroundColor Green
    } catch {
        Write-Host "Error al escanear el archivo: $_" -ForegroundColor Red
    }
}

Export-ModuleMember -Function escaneo
