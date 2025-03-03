# Путь к nginx.exe
$nginxPath = "D:\nginx-1.27.4\nginx.exe"

# Проверка, запущен ли уже Nginx
$nginxProcess = Get-Process nginx -ErrorAction SilentlyContinue
if ($nginxProcess) {
    Write-Host "Nginx уже запущен."
} else {
    # Создание директории logs, если она отсутствует
    $logsDir = "D:\nginx-1.27.4\logs"
    if (-not (Test-Path $logsDir)) {
        New-Item -ItemType Directory -Path $logsDir
        Write-Host "Директория logs создана: $logsDir"
    }

    # Запуск Nginx без указания конфигурационного файла (используется стандартный)
    Start-Process -FilePath $nginxPath -NoNewWindow
    Write-Host "Nginx запущен со стандартным конфигурационным файлом."
}

# Ожидание нажатия клавиши, чтобы окно не закрылось сразу
Write-Host "Нажмите любую клавишу, чтобы закрыть это окно..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")