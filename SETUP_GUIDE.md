# 🌹 Sara Match Bot - Setup & Deployment Qo'llanmasi

## 📋 Oldindan Tayyorlash

### 1. BotFather dan Bot Token olish

1. **Telegram da @BotFather ni toping**
2. `/start` yozing
3. `/newbot` bosin
4. Bot uchun nom va username berin
5. Token olasiz (BOT TOKEN)

**Misal Token:** `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`

### 2. Python o'rnatish (agar yuq bo'lsa)
```bash
# Windows
python --version  # Python 3.8+ kerak

# Linux/Mac
python3 --version
```

---

## 🚀 LOCAL TEST QILISH

### 1. Proyektni Setup qilish

```bash
# Papka yarating va kiriting
mkdir sara_match_bot
cd sara_match_bot

# Fayllarni ko'ching:
# - sara_match_bot.py
# - requirements.txt
# - .env.example

# .env faylini yarating
cp .env.example .env

# .env ni o'zingizning token bilan to'ldiring
# Windows: notepad .env
# Linux/Mac: nano .env
```

### 2. Paketlar o'rnatish

```bash
# Virtual environment yarating (ixtiyoriy)
python -m venv venv

# Aktivasiyon
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# Paketlar o'rnatish
pip install -r requirements.txt
```

### 3. Botni ishga tushirish

```bash
python sara_match_bot.py
```

**Xabar ko'rish kerak:**
```
🤖 Sara Match Bot ishga tushdi...
```

### 4. Telegram da test qilish

1. Telegram ochib, o'zingizning bot username ni qidiring
2. `/start` bosin
3. Profile yarating va test qiling!

---

## 🌐 RENDER ga Deploy qilish (BEPUL)

### 1. Github ga repozitoriy yarating

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/sara_match_bot.git
git branch -M main
git push -u origin main
```

**MUHIM:** `.gitignore` file yarating:
```
.env
sara_match.db
venv/
__pycache__/
.vscode/
```

### 2. Render.com ga register qilish

1. https://render.com ga kiriting
2. GitHub bilan login qiling
3. **New +** → **Web Service** bosing
4. GitHub repozitoriyni tanlang

### 3. Konfiguratsiyani qiling

**Build Settings:**
```
Build Command: pip install -r requirements.txt
Start Command: python sara_match_bot.py
```

**Environment Variables:**
```
BOT_TOKEN = YOUR_BOT_TOKEN_HERE
```

### 4. Deploy

1. **Create Web Service** bosing
2. 2-3 minut kutib turing
3. Deploy tamomlandi!

### 5. Keep-Alive (Bepul planida kerak)

Render bepul plan bir muddat foydalanilmasa, uyu qo'yadi. Buning uchun:

```bash
# sara_match_bot.py ga qo'shing:

import requests
import threading
import time

def keep_alive():
    """Render uyu qo'ymaslik uchun"""
    while True:
        try:
            requests.get(f"https://YOUR_APP_NAME.onrender.com", timeout=5)
            time.sleep(600)  # 10 minutda bir
        except:
            pass

# Main() da qo'shing:
threading.Thread(target=keep_alive, daemon=True).start()
```

---

## 🔒 RAILWAY ga Deploy qilish (Premium)

### 1. Railway.app ga kiriting

1. https://railway.app ga ochib, GitHub bilan login qiling
2. **New Project** → **Deploy from GitHub** bosing

### 2. Konfiguratsiya

`Procfile` file yarating:
```
worker: python sara_match_bot.py
```

`.env` ni qo'shing:
```
BOT_TOKEN=YOUR_TOKEN
```

### 3. Deploy

Avtomatik deploy bo'ladi!

---

## 💾 DATABASE BACKUP

### SQLite backup

```bash
# Lokalni SQL databaseni backup qilish
cp sara_match.db sara_match_backup.db
```

### Cloud DB (optional)

Agar cloud database foydalanmoqchi bo'lsangiz, kodni o'zgartirib PostgreSQL qo'llang:

```python
import psycopg2

conn = psycopg2.connect(
    host="db_host",
    database="db_name",
    user="db_user",
    password="db_pass"
)
```

---

## 🐛 PROBLEMALAR VA YECHIMI

### Problem: "ModuleNotFoundError: No module named 'telebot'"

**Yechim:**
```bash
pip install pyTelegramBotAPI
```

### Problem: Bot javob bermayapti

1. Token to'g'rimi? `.env` ni tekshiring
2. Internet ulanishni tekshiring
3. Bot ishlayaptimi? `python sara_match_bot.py` ishga tushiring

### Problem: Database xatoligi

```bash
# Database ni qayta yaratish
rm sara_match.db
python sara_match_bot.py
```

---

## 📞 TELEGRAM BOT API COMMANDS

Bot admin uchun (optional):

```
/start - Bot boshlash
/help - Qo'llanma
/ban @username - Foydalanuvchini bloklasch
/stats - Statistika ko'rish
```

---

## 🎯 KEYINGI QO'SHIMCHALAR (Future)

```python
# 1. Admin Panel
# 2. Ban/Report System
# 3. Email verification
# 4. Payments (Stripe/Payme)
# 5. Analytics Dashboard
# 6. AI Recommendations
# 7. Video Call (agora.io)
# 8. Story Upload (Instagram kabi)
```

---

## 📚 FOYDALI LINKLAR

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [PyTelegramBotAPI Docs](https://github.com/eternnoir/pyTelegramBotAPI)
- [Render Docs](https://render.com/docs)
- [Railway Docs](https://railway.app/docs)

---

**Savollar bo'lsa, ping bering! 🚀**
