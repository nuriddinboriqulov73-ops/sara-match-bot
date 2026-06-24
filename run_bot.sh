#!/bin/bash
# Sara Match Bot - Quick Start Script

echo "🌹 Sara Match Bot - Setup"
echo "========================"

# 1. Virtual Environment yaratish
echo "📦 Virtual environment yaratilmoqda..."
python -m venv venv

# Aktivasiyon
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Linux/Mac
    source venv/bin/activate
fi

# 2. Paketlar o'rnatish
echo "📥 Paketlar o'rnatilmoqda..."
pip install --upgrade pip
pip install -r requirements.txt

# 3. .env file yaratish
echo "🔑 .env file yaratilmoqda..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "❌ .env file yaratildi. Bot tokeningizni kiriting:"
    echo "   .env faylni text editor bilan ochib, BOT_TOKEN qiymatini o'zgartiring"
    echo ""
    read -p "Bot tokeningizni kiriting: " bot_token
    if [ ! -z "$bot_token" ]; then
        sed -i "s/YOUR_BOT_TOKEN_HERE/$bot_token/" .env
        echo "✅ Token saqlandi!"
    fi
else
    echo "✅ .env fayli allaqachon bor"
fi

# 4. Bot ishga tushirish
echo ""
echo "✨ Bot ishga tushmoshga tayyorlandi!"
echo ""
read -p "Botni ishga tushirmohchi? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Bot ishga tushmokda..."
    python sara_match_bot.py
else
    echo "⏹️  Otkazildi. Keyinroq 'python sara_match_bot.py' yozing"
fi
