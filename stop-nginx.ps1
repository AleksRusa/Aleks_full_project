# Проверка, запущен ли Nginx
$nginxProcess = Get-Process nginx -ErrorAction SilentlyContinue
if ($nginxProcess) {
    # Остановка Nginx
    Stop-Process -Name nginx -Force
    Write-Host "Nginx остановлен."
} else {
    Write-Host "Nginx не запущен."
}

# Ожидание нажатия клавиши, чтобы окно не закрылось сразу
Write-Host "Нажмите любую клавишу, чтобы закрыть это окно..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")