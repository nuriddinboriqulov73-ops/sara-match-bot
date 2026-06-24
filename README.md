# 🌹 Sara Match Bot - Telegram Tanishadigan Boti

Sara Match Bot - Telegram orqali yangi do'stlar topish uchun mo'ljallangan bot. Erkaklar va ayollarni o'zaro match qiladi va suhbatlashish imkonini beradi.

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Xususiyatlari

✅ **Profil Yaratish**
- Rasm, F.I.O, yosh, shahar
- Bio va qiziqishlari
- Jinsiy xususiyat va izlanish turi

✅ **Matching Tizimi**
- Erkak/Ayol matching
- Like/Reject sistema
- Agar ikkalasi like bosdi - MATCH!

✅ **Chat Sistema**
- Matched foydalanuvchilar o'rtasida suhbat
- Suhbat tarixi saqlash
- Real-time xabar yuborish

✅ **Admin Panel** (Advanced)
- Statistika ko'rish
- Foydalanuvchilarni boshqarish
- Report va Ban sistema
- Broadcast xabarlar

✅ **Database**
- SQLite (lokal) yoki PostgreSQL (cloud)
- Barcha ma'lumot shifrlash

---

## 🚀 TEZKOR BOSHLASH

### Windows

```bash
# run_bot.bat ni double-click qiling
run_bot.bat

# Yoki manually:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python sara_match_bot.py
```

### Linux/Mac

```bash
bash run_bot.sh

# Yoki manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 sara_match_bot.py
```

---

## 📋 PRE-REQUIREMENTS

- Python 3.8+ 
- Telegram Account
- BotFather dan Bot Token

### Bot Token olish

1. Telegram da `@BotFather` ni qidiring
2. `/start` yozing
3. `/newbot` bosin
4. Bot uchun nom va username berin
5. **Token** olasiz

**Misal:** `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`

---

## ⚙️ KONFIGURATSIYA

### 1. .env file ni to'ldirish

```bash
# .env.example ni .env ga copy qiling
cp .env.example .env

# .env ni editor bilan ochib:
BOT_TOKEN=YOUR_BOT_TOKEN_HERE
```

### 2. Optional: Admin ID qo'shish (Admin panel uchun)

`sara_match_bot.py` da:
```python
ADMIN_IDS = [YOUR_TELEGRAM_ID]  # Shu yerga o'zingizning ID qo'ying
```

ID ni topish:
1. @userinfobot ni Telegramda qidiring
2. `/start` bosin
3. ID ko'rinadi

---

## 📁 FILE TUZILISHI

```
sara_match_bot/
├── sara_match_bot.py          # Asosiy bot kodi
├── advanced_features.py       # Admin panel, stats
├── requirements.txt           # Python paketlari
├── .env.example              # Config namunasi
├── .env                       # Config (siri)
├── .gitignore                # Git ignore fayllar
├── sara_match.db             # Database (auto create)
├── run_bot.sh                # Linux/Mac start script
├── run_bot.bat               # Windows start script
├── SETUP_GUIDE.md            # Batafsil setup
└── README.md                 # Bu fayl

```

---

## 🎮 BOT COMMANDS

### Foydalanuvchi Commandlari

| Command | Tavsif |
|---------|--------|
| `/start` | Botni boshlash |
| `/help` | Qo'llanma |

### Admin Commandlari

| Command | Tavsif |
|---------|--------|
| `/admin` | Admin panelni ochish |
| Statistika | Foydalanuvchi stats |
| Broadcast | Barcha foydalanuvchilarga xabar |

---

## 🌐 CLOUD DEPLOYMENT

### Render.com (BEPUL) ✨

1. GitHub repozitoriy yarating
2. https://render.com ga login qiling
3. New Web Service yarating
4. GitHub repozitoriyni tanlang
5. Start Command: `python sara_match_bot.py`
6. BOT_TOKEN environment variable qo'shing

**Natija:** 24/7 ishlaydigan bot!

### Railway.app (Premium)

1. https://railway.app ga kiriting
2. New Project yarating
3. GitHub repozitoriyni tanlang
4. Environment variables qo'shing
5. Auto deploy!

### Heroku (To'lanadi, lekin popular)

```bash
heroku create sara-match-bot
heroku config:set BOT_TOKEN=YOUR_TOKEN
git push heroku main
```

---

## 📊 DATABASE SCHEMA

### Users Table
```sql
- id (PRIMARY KEY)
- telegram_id (UNIQUE)
- full_name
- age
- gender
- city
- bio
- photo_id
- interests
- looking_for
- created_at
- status (active/banned)
```

### Likes Table
```sql
- id (PRIMARY KEY)
- from_user_id (FK)
- to_user_id (FK)
- action (like/reject)
- created_at
```

### Matches Table
```sql
- id (PRIMARY KEY)
- user1_id (FK)
- user2_id (FK)
- matched_at
- UNIQUE(user1_id, user2_id)
```

### Messages Table
```sql
- id (PRIMARY KEY)
- match_id (FK)
- from_user_id (FK)
- to_user_id (FK)
- message
- created_at
```

---

## 🔧 ADVANCED FEATURES

### Admin Panel

`sara_match_bot.py` ga qo'shing:
```python
from advanced_features import register_admin_handlers
register_admin_handlers(bot)
```

Keyin `/admin` bosin.

### Email Verification

```python
from advanced_features import require_email_verification

token = require_email_verification(user_id, email)
# Email ga verification link yuboring
```

### Profile Score

```python
from advanced_features import get_profile_score

score = get_profile_score(user_id)
print(f"Profile {score}% to'liq")
```

---

## 🐛 PROBLEMALAR VA YECHIMI

### "Token invalid"
- Token to'g'rimi? `.env` ni tekshiring
- BotFather dan yangi token oling

### Bot javob bermayapti
- Internet ulanish tekshiring
- `python sara_match_bot.py` ishga tushitishni tekshiring

### Database xatosi
```bash
# Database ni qayta yaratish
rm sara_match.db
python sara_match_bot.py
```

### Virtual environment problema
```bash
# Virtual env ni qayta yaratish
rm -rf venv
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
```

---

## 📈 OPTIMIZATION VA SCALING

### 1. Database Optimization

Large user (10k+) uchun PostgreSQL ishlatish:
```python
import psycopg2

conn = psycopg2.connect(
    host="db.example.com",
    database="sara_match",
    user="user",
    password="pass"
)
```

### 2. Caching

Redis cache:
```python
import redis

cache = redis.Redis(host='localhost', port=6379)
cache.set('user:123', json.dumps(user_data))
```

### 3. Load Balancing

Multi-process bot:
```python
import multiprocessing

if __name__ == '__main__':
    processes = [
        multiprocessing.Process(target=bot.infinity_polling)
        for _ in range(4)
    ]
    for p in processes:
        p.start()
```

---

## 🔒 SECURITY

### Best Practices

✅ `.env` file ishlatish (tokens uchun)
✅ SQL injection protection (prepared statements)
✅ Rate limiting (spam to'xtatish)
✅ Input validation
✅ HTTPS (deployment da)

### Misol: Rate Limiting

```python
from time import time

user_requests = {}

def is_rate_limited(user_id, limit=10, window=60):
    now = time()
    if user_id not in user_requests:
        user_requests[user_id] = []
    
    user_requests[user_id] = [
        t for t in user_requests[user_id] 
        if now - t < window
    ]
    
    if len(user_requests[user_id]) >= limit:
        return True
    
    user_requests[user_id].append(now)
    return False
```

---

## 📚 FOYDALI LINKLAR

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [PyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
- [Render Docs](https://render.com/docs)
- [Railway Docs](https://railway.app/docs)
- [SQLite Docs](https://www.sqlite.org/docs.html)

---

## 🤝 QARAM OLISH

Suhbatlar va matching data:
```python
# Advanced filtering
from advanced_features import get_filtered_profiles

profiles = get_filtered_profiles(
    user_id=123,
    age_min=18,
    age_max=50,
    distance_km=50
)
```

---

## 📞 SUPPORT

Savollar yoki bugs uchun:
- GitHub Issues ochib savolingizni yozing
- Discord serverga qo'shiling (link: tbd)

---

## 📜 LICENSE

MIT License - Ishlating!

```
MIT License

Copyright (c) 2024 Sara Match Bot

Permission is hereby granted, free of charge...
```

---

## 🎯 ROADMAP

- [ ] Video Call Integration (Agora.io)
- [ ] Stories (Instagram kabi)
- [ ] Verified Badges
- [ ] Subscription Model
- [ ] AI Recommendations
- [ ] Payment Integration (Stripe)
- [ ] Multi-language Support
- [ ] Mobile App (React Native)

---

## 🙌 CONTRIBUTORS

Bu loyihaga hissa qo'shmoqchi bo'lsangiz, fork qiling va PR yuboring!

---

**Made with ❤️ for making connections**

🌹 Sara Match Bot - Shuning uchun tuzilgan! 🌹

