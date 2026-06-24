# 🌹 Sara Match Bot - SETUP CHECKLIST

## ✅ PRE-REQUIREMENTS CHECK

### Kompyuteringizda bor ekanligini tekshiring:

- [ ] Python 3.8+ o'rnatilgan (`python --version`)
- [ ] Git o'rnatilgan (optional, lekin tavsiya)
- [ ] Text editor (VS Code, Notepad++, vb.)
- [ ] Telegram akkaunt
- [ ] Internet ulanishi

---

## 🚀 SETUP STAGES

### STAGE 1: BOT TOKEN OLISH (15 minutes)

**✓ Qadamlar:**

1. [ ] Telegram da **@BotFather** qidiring
2. [ ] `/start` yozing
3. [ ] `/newbot` bosin
4. [ ] Bot uchun nom berin (Mesala: "Sara Match Test")
5. [ ] Bot uchun **@username** berin (Mesala: "@saratest123bot")
6. [ ] **TOKEN** olasiz (Masalan: "123456:ABCdefGHIJKL-zyx")
7. [ ] Tokenni copy qilib qo'ying

**Natija:** Bot token qo'lingizda bor ✅

---

### STAGE 2: PROYEKTNI SETUP QILISH (10 minutes)

**✓ Qadamlar:**

1. [ ] Yangi folder yarating (Mesala: `C:\Users\User\Desktop\sara_match_bot`)
2. [ ] Bu fayllarni shu folder-ga ko'ching:
   - [ ] sara_match_bot.py
   - [ ] requirements.txt
   - [ ] .env.example
   - [ ] run_bot.bat (Windows uchun)
   - [ ] run_bot.sh (Linux/Mac uchun)

3. [ ] `.env.example` ni `.env` ga rename qiling
4. [ ] `.env` faylini editor bilan ochib:
   - [ ] `BOT_TOKEN=YOUR_BOT_TOKEN_HERE` o'rnini o'z tokeningiz bilan almashting

**Misal .env fayli:**
```
BOT_TOKEN=123456:ABCdefGHIJKL-zyx57W2v1u123ew11
```

**Natija:** Proyekt setup bo'ldi ✅

---

### STAGE 3: BOT ISHGA TUSHIRISH (5 minutes)

#### WINDOWS

```bash
# Option 1: Oson (double-click)
run_bot.bat

# Option 2: Manual
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python sara_match_bot.py
```

#### LINUX / MAC

```bash
# Option 1: Oson (bash)
bash run_bot.sh

# Option 2: Manual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 sara_match_bot.py
```

**Kutilgan Result:**
```
🤖 Sara Match Bot ishga tushdi...
```

**Natija:** Bot online ✅

---

### STAGE 4: BOT TEST QILISH (5 minutes)

1. [ ] Telegram ochib, o'zingizning bot username ni qidiring
   - Mesala: "@saratest123bot"

2. [ ] Bot-ga kirish
   - [ ] `/start` bosin
   - [ ] "Profile yaratish" bosin

3. [ ] Profile to'ldiring:
   - [ ] F.I.O kiriting
   - [ ] Yosh kiriting
   - [ ] Jinsiy xususiyat tanlang
   - [ ] Shahar kiriting
   - [ ] Bio yozing
   - [ ] Izlanish turi tanlang
   - [ ] Qiziqishlari yozing
   - [ ] Rasm yuklang (har qanday rasm)

4. [ ] Main menu ga qaytish
5. [ ] "Matching" bosin
6. [ ] Profile ko'rinish

**Natija:** Bot to'liq ishlaydi ✅

---

## ☁️ CLOUD DEPLOYMENT (Optional)

### Render.com ga Deploy (BEPUL)

#### STAGE 5: GITHUB REPOZITORIY YARATISH

1. [ ] https://github.com ga login qiling (akkaunt bo'lmasa register qiling)
2. [ ] **New repository** yarating
   - [ ] Repository name: "sara-match-bot"
   - [ ] "Add .gitignore" → "Python" tanlang
   - [ ] "Create repository" bosin

3. [ ] Local folderingizda:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/sara-match-bot.git
   git branch -M main
   git push -u origin main
   ```

**Natija:** Kod GitHub-da ✅

#### STAGE 6: RENDER-GA DEPLOY

1. [ ] https://render.com ga kiriting
2. [ ] GitHub bilan login qiling
3. [ ] **New** → **Web Service**
4. [ ] GitHub repozitoriyni tanlang
5. [ ] Settings:
   - [ ] Name: "sara-match-bot"
   - [ ] Build Command: `pip install -r requirements.txt`
   - [ ] Start Command: `python sara_match_bot.py`
   - [ ] Environment: "Python 3"

6. [ ] **Environment** tab:
   - [ ] **Key:** `BOT_TOKEN`
   - [ ] **Value:** YOUR_TOKEN_HERE
   - [ ] **Add** bosin

7. [ ] **Create Web Service** bosin
8. [ ] Deploy kutish (2-3 minut)

**Natija:** Bot 24/7 online ✅

---

## 🔧 ADMIN PANEL SETUP (Advanced)

1. [ ] O'zingizning Telegram ID ni topish:
   - [ ] Telegram da **@userinfobot** qidiring
   - [ ] `/start` bosin
   - [ ] ID ko'rinadi

2. [ ] `sara_match_bot.py` ni ochib:
   ```python
   ADMIN_IDS = [YOUR_TELEGRAM_ID]  # Shu yerga ID qo'ying
   ```

3. [ ] Saqlang va bot-ni restart qiling

4. [ ] Telegram-da bot-ga `/admin` yozing
   - [ ] Admin menu ko'rinishi kerak

**Natija:** Admin panel ishlaydi ✅

---

## 📊 OPTIONAL FEATURES

### Advanced Features Ishlatish

1. [ ] `advanced_features.py` ni shu folder-ga kopialay qiling
2. [ ] `sara_match_bot.py` ga qo'shing:
   ```python
   from advanced_features import register_admin_handlers
   register_admin_handlers(bot)
   ```

3. [ ] Bot-ni restart qiling
4. [ ] `/admin` bosin → yangi features ko'rinadi

**Features:**
- [ ] Statistics dashboard
- [ ] User management
- [ ] Broadcast messages
- [ ] Ban system

---

## 🐛 TROUBLESHOOTING

### Problem: "Bot javob bermayapti"

**Yechim:**
- [ ] Internet ulanishni tekshiring
- [ ] `.env` file-da token to'g'rimi?
- [ ] Konsol-da xatolar bormi?
- [ ] Token active emasmi? BotFather-dan tokenni regenerate qiling

### Problem: "Port already in use"

**Yechim:**
```bash
# Eski processni to'xtatish
# Windows:
taskkill /F /IM python.exe

# Linux/Mac:
pkill -f sara_match_bot.py
```

### Problem: "ModuleNotFoundError"

**Yechim:**
```bash
# Virtual environment ni tekshiring
pip install -r requirements.txt

# Yoki qayta yaratish
rm -rf venv
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
```

### Problem: "Database locked"

**Yechim:**
```bash
# Bot-ni to'xtatib:
rm sara_match.db
# Bot-ni restart qiling - yangi database yaratiladi
```

---

## ✨ FINAL CHECKLIST

### Deployment Before Production

- [ ] Bot tokenni secure saqlading
- [ ] .env file-da .gitignore-da
- [ ] Database backup olingiz
- [ ] Admin ID to'g'ri set qildingi
- [ ] Test profile bar
- [ ] Matching ishlaydi
- [ ] Chat ishlaydi
- [ ] Cloud deploy qildingiz (opsional)
- [ ] Keep-alive setup qildingiz (Render uchun)
- [ ] README.md o'qidingiz
- [ ] Bot social media-da e'lon qildingiz 📢

---

## 🎉 TUBANDAMANA!

**Tabriklaymiz!** 🌹 Sara Match Bot ready for production!

### Keyingi Qadamlar:

1. **Marketing:** Foydalanuvchilarni invite qiling
2. **Monitoring:** Regular backup oling
3. **Updates:** Bot features-ni upgrade qiling
4. **Feedback:** Foydalanuvchilar feedback-ini tinglang
5. **Scaling:** Foydalanuvchi ko'paysa, database upgrade qiling

---

## 📞 HELP & SUPPORT

Savollar bo'lsa:
- GitHub Issues ochib savolingizni yozing
- README.md tekshiring
- SETUP_GUIDE.md o'qing
- Advanced_features.py docs ko'ring

---

**🌹 Muvaffaqiyat tilaymiz! 🌹**

Happy matching! 💕

