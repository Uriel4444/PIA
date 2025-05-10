
<#
bloquear_ips.ps1
----------------------------------------
Lee ips_maliciosos.csv.  Por cada IP con 'SI' en la
columna Es_maliciosa, crea (si no existe) una regla
de firewall que la bloquee en sentido outbound.
Luego guarda de nuevo el CSV añadiendo la columna
Bloqueada (SI / NO) y muestra el SHA‑256 final.

Uso:
    powershell -ExecutionPolicy Bypass -File bloquear_ips.ps1 -Csv ips_maliciosos.csv
----------------------------------------#>

param(
    [Parameter(Mandatory)][string]$Csv
)

if (-not (Test-Path $Csv)) {
    Write-Host "CSV no encontrado: $Csv"
    exit
}

# Carga de registros del CSV
$rows = Import-Csv $Csv
foreach ($row in $rows) {
    if ($row.Es_maliciosa -eq "SI") {
        $ip   = $row.IP
        $rule = "Block_$ip"

        if (-not (Get-NetFirewallRule -DisplayName $rule -ErrorAction SilentlyContinue)) {
            # Crea regla outbound para bloquear la IP
            New-NetFirewallRule -DisplayName $rule -Direction Outbound -RemoteAddress $ip `
                                -Action Block -Protocol Any | Out-Null
        }
        $row.Bloqueada = "SI"
    } else {
        $row.Bloqueada = "NO"
    }
}

# Vuelve a guardar el CSV con la nueva columna
$rows | Export-Csv $Csv -NoTypeInformation

# Hash y resumen
$hash = (Get-FileHash $Csv -Algorithm SHA256).Hash
Write-Host "CSV actualizado: $(Resolve-Path $Csv)"
Write-Host "SHA-256       : $hash"
Write-Host "Fecha         : $(Get-Date -Format s)"
