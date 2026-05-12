@echo off
echo Starting Backend Server...
cd backend
start cmd /k "python app.py"

echo Starting Mock Data Sender...
start cmd /k "python mock_sender.py"

echo Starting Frontend Server...
cd ../frontend
start cmd /k "python -m http.server 8000"

echo.
echo All services started!
echo Open your browser and navigate to: http://localhost:8000/dashboard.html
pause
