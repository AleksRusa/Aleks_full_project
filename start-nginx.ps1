# Путь к папке с Nginx
$nginxPath = "D:\Program Files\nginx\nginx-1.26.3"

# Проверка, запущен ли уже Nginx
$nginxProcess = Get-Process nginx -ErrorAction SilentlyContinue
if ($nginxProcess) {
    Write-Host "Nginx уже запущен."
} else {
    # Запуск Nginx
    Start-Process -FilePath "$nginxPath\nginx.exe" -NoNewWindow
    Write-Host "Nginx запущен. Проверьте http://localhost"
}

# Ожидание нажатия клавиши, чтобы окно не закрылось сразу
Write-Host "Нажмите любую клавишу, чтобы закрыть это окно..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")