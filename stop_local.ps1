# MarketMind AI - Stop Local Services
Write-Host "Stopping all MarketMind AI local services (Ports 8000, 5000, 5002, 8501)..." -ForegroundColor Yellow

$ports = @(8000, 5000, 5002, 8501)
foreach ($port in $ports) {
    $processes = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
    if ($processes) {
        foreach ($pidToKill in $processes) {
            Write-Host "Killing process $pidToKill on port $port" -ForegroundColor Red
            Stop-Process -Id $pidToKill -Force -ErrorAction SilentlyContinue
        }
    } else {
        Write-Host "Port $port is clear." -ForegroundColor Green
    }
}
Write-Host "All local services stopped." -ForegroundColor Green
