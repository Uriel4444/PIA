function procesos_maliciosos {
    param ()

    $headers = $global:headers
    $procesos = Get-Process | Where-Object { $_.Path } | Select-Object Name, Id, Path
    $rutas = $procesos | Select-Object -ExpandProperty Path

    $total = $rutas.Count
    $actual = 1

    foreach ($ruta in $rutas) {
        Write-Host "`n[$actual/$total] Escaneando: $ruta" -ForegroundColor Cyan
        Start-Sleep -Seconds 20
        try {
            $hash = (Get-FileHash -Path $ruta).Hash
            $url = "https://www.virustotal.com/api/v3/files/$hash"
            $respuesta = Invoke-RestMethod -Uri $url -Headers $headers -Method Get
            $malicioso = $respuesta.data.attributes.last_analysis_stats.malicious

            if ($malicioso -gt 0) {
                Write-Host "Posible malware en $ruta" -ForegroundColor Red
                Write-Host "El hash es: $hash"
                Write-Host "URL: https://www.virustotal.com/gui/file/$hash"
            }
        } catch {
            if ($_.ErrorDetails.Message -like '*QuotaExceededError*') {
                Write-Host "Se ha alcanzado el límite de peticiones por minuto (4/min)" -ForegroundColor Red
                Start-Sleep -Seconds 60
            } else {
                Write-Host "Error al consultar el archivo $ruta" -ForegroundColor Red
            }
        }
        $actual++
    }
}

Export-ModuleMember -Function procesos_maliciosos
