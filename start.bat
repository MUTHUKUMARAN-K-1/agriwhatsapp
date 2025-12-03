@echo off
echo Starting WhatsApp Agent...
echo.

REM Activate virtual environment
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

REM Check if .env exists
if not exist ".env" (
    echo ERROR: .env file not found!
    echo Please create .env file with your API keys
    pause
    exit /b 1
)

echo Starting Flask server on port 5000...
echo.
echo ========================================
echo   WhatsApp Agent Running
echo ========================================
echo   Local: http://localhost:5000
echo   Test: http://localhost:5000/test
echo.
echo Press Ctrl+C to stop
echo ========================================
echo.

python app.py
