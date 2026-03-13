@echo off
echo ========================================
echo Healthcare Mobile App - Quick Setup
echo ========================================
echo.

echo Step 1: Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment created
echo.

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

echo Step 3: Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

echo Step 4: Creating cache directory...
if not exist "cache" mkdir cache
echo ✓ Cache directory created
echo.

echo Step 5: Creating temp directory...
if not exist "temp" mkdir temp
echo ✓ Temp directory created
echo.

echo ========================================
echo Setup Complete! 🎉
echo ========================================
echo.
echo To run the app:
echo   1. Activate virtual environment: venv\Scripts\activate
echo   2. Run: python main.py
echo.
echo To build for Android:
echo   buildozer -v android debug
echo.
echo For more information, see README.md
echo.
pause
