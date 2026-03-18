@echo off
title Система доставки
color 0A
 
echo.
echo  ================================
echo   СИСТЕМА ДОСТАВКИ — ЗАПУСК
echo  ================================
echo.
 
cd /d "%~dp0"
 
if not exist "node_modules\" (
    echo  [!] node_modules не знайдено. Встановлюємо залежності...
    call npm install
    echo.
)
 
echo  [OK] Запускаємо сервер...
echo  [OK] Відкрийте браузер: http://localhost:3000
echo.
echo  Для зупинки натисніть Ctrl+C
echo.
 
start "" timeout /t 2 /nobreak >nul
start "" "http://localhost:3000"
 
node server.js
 
pause
