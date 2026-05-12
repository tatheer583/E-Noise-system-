@echo off
setlocal
echo ==========================================
echo    SMART E-NOSE AI SYSTEM BOOTSTRAP
echo ==========================================

echo [1/3] Starting Backend API...
cd backend
start "E-Nose Backend" cmd /k "..\venv\Scripts\python app.py"

echo [2/3] Starting Mock Data Simulator...
start "E-Nose Simulator" cmd /k "..\venv\Scripts\python mock_sender.py"

echo [3/3] Starting Frontend Dashboard...
cd ../frontend
start "E-Nose Frontend" cmd /k "python -m http.server 8000"

echo.
echo ------------------------------------------
echo SUCCESS: All subsystems are launching!
echo Dashboard: http://localhost:8000/dashboard.html
echo ------------------------------------------
pause
