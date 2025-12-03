@echo off
echo ========================================
echo   WhatsApp Agent - Twilio Quick Setup
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "app.py" (
    echo ERROR: Please run this script from the "Whatsapp Agent" directory
    pause
    exit /b 1
)

echo Step 1: Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment created
echo.

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

echo Step 3: Upgrading pip...
python -m pip install --upgrade pip --quiet
echo ✓ Pip upgraded
echo.

echo Step 4: Installing dependencies...
echo This may take a few minutes...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo WARNING: Some packages may have failed to install
    echo This is OK - PyAudio is optional
)
echo ✓ Dependencies installed
echo.

echo Step 5: Creating .env file...
if exist ".env" (
    echo .env file already exists, skipping...
) else (
    copy .env.example .env
    echo ✓ .env file created
    echo.
    echo IMPORTANT: You need to edit .env and add your API keys:
    echo   - GEMINI_API_KEY
    echo   - ELEVENLABS_API_KEY
    echo   - TWILIO_ACCOUNT_SID
    echo   - TWILIO_AUTH_TOKEN
    echo.
    echo Opening .env file for editing...
    timeout /t 2 /nobreak >nul
    notepad .env
)

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Make sure you've added all API keys to .env
echo 2. Run: python app.py
echo 3. In another terminal, run: ngrok http 5000
echo 4. Configure Twilio webhook with ngrok URL
echo.
echo To start the app, run:
echo    venv\Scripts\activate
echo    python app.py
echo.
pause
