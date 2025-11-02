@echo off
echo ========================================
echo Multi-Agent Research Assistant
echo Web Interface Launcher
echo ========================================
echo.

cd /d "%~dp0"

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo.
echo Installing/updating dependencies...
python -m pip install -q --upgrade pip
python -m pip install -q -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo ========================================
echo Starting Web Interface...
echo ========================================
echo.
echo The interface will open in your browser at:
echo http://localhost:8501
echo.
echo To share with colleagues on your network, use:
echo Network URL (shown below)
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python -m streamlit run app.py

pause
