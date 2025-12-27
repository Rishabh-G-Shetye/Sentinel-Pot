@echo off
cd /d "%~dp0"
TITLE Sentinel-Pot Launcher
cls

echo ==========================================
echo    🛡️ SENTINEL-POT SECURITY SYSTEM
echo ==========================================

:: Step 0: Pre-flight checks
if not exist "ngrok.exe" (
    echo [!] ERROR: ngrok.exe not found!
    pause
    exit
)
if not exist "ngrok.yml" (
    echo [!] ERROR: ngrok.yml not found!
    echo     Please create the file with your tunnels configuration.
    pause
    exit
)
if not exist "pcaps" mkdir pcaps
if not exist "attacks.json" type nul > attacks.json

:: Step 1: Cleanup Ports
echo [*] Cleaning ports and old containers...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8080') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :2222') do taskkill /F /PID %%a 2>nul
taskkill /F /IM ngrok.exe >nul 2>&1
docker compose down >nul 2>&1

:: Step 2: Start Docker
echo [*] Starting Docker Swarm...
docker compose up -d --build

:: Step 3: Wait for Dashboard
echo [*] Waiting for Dashboard...
:loop
curl -s http://localhost:8501 >nul
if %ERRORLEVEL% NEQ 0 (
    timeout /t 2 >nul
    goto loop
)
echo [!] Dashboard LIVE at http://localhost:8501
start http://localhost:8501

:: Step 4: Start Ngrok using the YAML file
echo [*] Initializing Global Tunnels from ngrok.yml...
:: We use 'start --all' to launch everything defined in your yml
start "Sentinel Tunnels" cmd /k "ngrok.exe start --all --config=ngrok.yml"

echo ==========================================
echo    SYSTEM FULLY ARMED
echo ==========================================
echo  1. Check the NEW window titled "Sentinel Tunnels".
echo  2. It will list both your HTTP and TCP addresses.
echo  3. Copy the TCP address (e.g., 0.tcp.ngrok.io:12345) for SSH attacks.
echo  4. Copy the HTTP address (e.g., https://xyz.ngrok-free.app) for Web attacks.
echo ==========================================
pause

echo [*] Shutting down...
taskkill /F /IM ngrok.exe >nul 2>&1
docker compose down