@echo off
REM Sara Match Bot - Windows Quick Start

echo.
echo 🌹 Sara Match Bot - Windows Setup
echo ===================================
echo.

REM 1. Virtual Environment yaratish
echo 📦 Virtual environment yaratilmoqda...
if not exist venv (
    python -m venv venv
) else (
    echo ✅ Virtual environment mavjud
)

REM 2. Aktivasiyon
echo 📝 Virtual environment activate qilinyapti...
call venv\Scripts\activate.bat

REM 3. Paketlar o'rnatish
echo 📥 Paketlar o'rnatilmoqda...
pip install --upgrade pip
pip install -r requirements.txt

REM 4. .env file yaratish
echo.
echo 🔑 Konfiguratsiya setup...
if not exist ".env" (
    copy .env.example .env
    echo.
    echo ❌ .env file yaratildi!
    echo ⚠️  Bot tokeningizni kiriting:
    echo.
    echo    1. .env faylini notepad bilan ochib
    echo    2. BOT_TOKEN = YOUR_BOT_TOKEN_HERE
    echo    3. YOUR_BOT_TOKEN_HERE o'rniga token qo'ying
    echo    4. File ni saqlang (Ctrl+S)
    echo.
    pause
) else (
    echo ✅ .env fayli allaqachon configured
)

REM 5. Bot ishga tushirish
echo.
echo ✨ Setup tamomlandi!
echo.
set /p response="Botni ishga tushirmohchi? (y/n): "

if "%response%"=="y" (
    cls
    echo 🚀 Sara Match Bot ishga tushmokda...
    echo.
    python sara_match_bot.py
) else if "%response%"=="Y" (
    cls
    echo 🚀 Sara Match Bot ishga tushmokda...
    echo.
    python sara_match_bot.py
) else (
    echo.
    echo ⏹️  Otkazildi!
    echo.
    echo Keyinroq ishga tushirish uchun:
    echo    1. cmd.exe ochib
    echo    2. python sara_match_bot.py yozing
    echo.
    pause
)
