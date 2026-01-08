@echo off
echo ================================
echo Cyberpunk Discord Bot - Starting
echo ================================
echo.

REM Check if token.json exists
if not exist "token.json" (
    echo ERROR: token.json not found!
    echo.
    echo Please create a token.json file with the following format:
    echo {
    echo   "discord_token": "YOUR_BOT_TOKEN_HERE",
    echo   "owner_token": YOUR_DISCORD_USER_ID,
    echo   "auth_key": "YOUR_AUTH_KEY_HERE",
    echo   "bot_name": "YOUR_BOT_NAME_HERE"
    echo }
    echo.
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo Installing required Python packages...
pip install -r requirements.txt


echo Starting bot...
echo.

REM Run the bot
python Kitty.py

REM If bot exits, pause to see any error messages
echo.
echo Bot has stopped.
pause