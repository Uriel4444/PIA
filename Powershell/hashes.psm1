function analizar_hash {
    param (
        [Parameter(Mandatory=$true)]
        [string]$ruta_archivo
    )

    $headers = $global:headers

    if (-not (Test-Path $ruta_archivo)) {
        Write-Host "El archivo no existe" -ForegroundColor Red
        return
    }

    $hash = (Get-FileHash -Path $ruta_archivo).Hash
    Write-Host "El hash del archivo es: $hash" -ForegroundColor Green
    $url = "https://www.virustotal.com/api/v3/files/$hash"

    try {
        $respuesta = Invoke-RestMethod -Uri $url -Headers $headers -Method Get
        Write-Host "============RESULTADO=============" -ForegroundColor Green
        $respuesta.data.attributes.last_analysis_stats | Format-List
        Write-Host "===================================" -ForegroundColor Green
    } catch {
        Write-Host "No se pudo obtener el resultado del escaneo: $_" -ForegroundColor Red
    }
}

Export-ModuleMember -Function analizar_hash
