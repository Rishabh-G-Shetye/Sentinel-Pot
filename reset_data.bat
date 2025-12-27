@echo off
cd /d "%~dp0"
TITLE Sentinel-Pot Data Wiper
cls

echo ==========================================
echo    🧹 CLEANING SENTINEL-POT DATA
echo ==========================================

:: Step 1: Stop everything to release file locks
echo [*] Stopping Docker containers...
docker compose down >nul 2>&1
taskkill /F /IM ngrok.exe >nul 2>&1

:: Step 2: Delete Data Files
echo [*] Wiping logs...
if exist attacks.json del /F /Q attacks.json
if exist enriched_attacks.json del /F /Q enriched_attacks.json

:: Step 3: Clear PCAPs
echo [*] Clearing packet captures...
if exist pcaps\*.pcap del /F /Q pcaps\*.pcap

:: Step 4: Recreate empty files (prevents errors on startup)
type nul > attacks.json

echo.
echo [✓] System is clean.
echo.
echo Press any key to start the system again...
pause >nul

:: Step 5: Auto-launch
call launch_sentinel.bat