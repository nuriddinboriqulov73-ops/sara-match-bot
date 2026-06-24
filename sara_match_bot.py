import telebot
from telebot.types import (
    InlineKeyboardMarkup, InlineKeyboardButton, 
    ReplyKeyboardMarkup, KeyboardButton, User
)
import sqlite3
from datetime import datetime
import json
import os

# Bot tokeningizni shu yerga qo'ying
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
bot = telebot.TeleBot(BOT_TOKEN)

# ================== DATABASE SETUP ==================

def init_db():
    """Database ni initialize qilish"""
    conn = sqlite3.connect('sara_match.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        telegram_id INTEGER UNIQUE,
        full_name TEXT,
        age INTEGER,
        gender TEXT,
        city TEXT,
        bio TEXT,
        photo_id TEXT,
        interests TEXT,
        looking_for TEXT,
        created_at TIMESTAMP,
        status TEXT DEFAULT 'active'
    )
    ''')
    
    # Likes table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS likes (
        id INTEGER PRIMARY KEY,
        from_user_id INTEGER,
        to_user_id INTEGER,
        action TEXT,
        created_at TIMESTAMP,
        FOREIGN KEY(from_user_id) REFERENCES users(telegram_id),
        FOREIGN KEY(to_user_id) REFERENCES users(telegram_id)
    )
    ''')
    
    # Matches table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY,
        user1_id INTEGER,
        user2_id INTEGER,
        matched_at TIMESTAMP,
        FOREIGN KEY(user1_id) REFERENCES users(telegram_id),
        FOREIGN KEY(user2_id) REFERENCES users(telegram_id),
        UNIQUE(user1_id, user2_id)
    )
    ''')
    
    # Messages table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY,
        match_id INTEGER,
        from_user_id INTEGER,
        to_user_id INTEGER,
        message TEXT,
        created_at TIMESTAMP,
        FOREIGN KEY(match_id) REFERENCES matches(id),
        FOREIGN KEY(from_user_id) REFERENCES users(telegram_id),
        FOREIGN KEY(to_user_id) REFERENCES users(telegram_id)
    )
    ''')
    
    conn.commit()
    conn.close()

def get_db():
    """Database connection"""
    conn = sqlite3.connect('sara_match.db')
    conn.row_factory = sqlite3.Row
    return conn

# ================== USER PROFILE ==================

user_data = {}

@bot.message_handler(commands=['start'])
def start_handler(message):
    """Botni boshlash"""
    user_id = message.chat.id
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        send_main_menu(user_id)
    else:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("👤 Profile yaratish", callback_data="create_profile"))
        bot.send_message(
            user_id,
            "🌹 *Sara Match ga xush kelibsiz!*\n\n"
            "Bu bot sizga yangi do'stlar topishga yordam beradi.\n"
            "Keling, boshlaylik!",
            parse_mode="Markdown",
            reply_markup=markup
        )

def send_main_menu(user_id):
    """Asosiy menu"""
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("❤️ Matching", callback_data="start_matching"),
        InlineKeyboardButton("💬 Suhbatlar", callback_data="my_chats")
    )
    markup.add(
        InlineKeyboardButton("👤 Profilim", callback_data="view_profile"),
        InlineKeyboardButton("⚙️ Sozlamalar", callback_data="settings")
    )
    markup.add(InlineKeyboardButton("ℹ️ Qo'llanma", callback_data="help"))
    
    bot.send_message(user_id, "🏠 *Asosiy Menu*", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "create_profile")
def create_profile_start(call):
    """Profile yaratishni boshlash"""
    user_id = call.message.chat.id
    user_data[user_id] = {}
    
    msg = bot.send_message(user_id, "👤 *F.I.O.*\n\nIsmingizni kiriting:")
    bot.register_next_step_handler(msg, get_full_name)

def get_full_name(message):
    """To'liq ism olish"""
    user_id = message.chat.id
    user_data[user_id]['full_name'] = message.text
    
    msg = bot.send_message(user_id, "🎂 *Yoshingiz*\n\nYoshingizni kiriting (raqam):")
    bot.register_next_step_handler(msg, get_age)

def get_age(message):
    """Yosh olish"""
    user_id = message.chat.id
    try:
        user_data[user_id]['age'] = int(message.text)
    except:
        msg = bot.send_message(user_id, "❌ Iltimos, to'g'ri raqam kiriting:")
        bot.register_next_step_handler(msg, get_age)
        return
    
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("👨 Erkak", "👩 Ayol")
    msg = bot.send_message(user_id, "👨‍👩 *Jinsiniz*", reply_markup=markup)
    bot.register_next_step_handler(msg, get_gender)

def get_gender(message):
    """Jinsiy xususiyet olish"""
    user_id = message.chat.id
    user_data[user_id]['gender'] = message.text
    
    msg = bot.send_message(user_id, "🏙️ *Shahar*\n\nQaysi shaharda yasaysiz?")
    bot.register_next_step_handler(msg, get_city)

def get_city(message):
    """Shahar olish"""
    user_id = message.chat.id
    user_data[user_id]['city'] = message.text
    
    msg = bot.send_message(user_id, "📝 *O'zingiz haqida*\n\nQisqacha ma'lumot yozing (bio):")
    bot.register_next_step_handler(msg, get_bio)

def get_bio(message):
    """Bio olish"""
    user_id = message.chat.id
    user_data[user_id]['bio'] = message.text
    
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("👨 Erkak", "👩 Ayol", "Farqi yo'q")
    msg = bot.send_message(user_id, "🔍 *Kimni qidiryapsiz?*", reply_markup=markup)
    bot.register_next_step_handler(msg, get_looking_for)

def get_looking_for(message):
    """Qidirish turi olish"""
    user_id = message.chat.id
    user_data[user_id]['looking_for'] = message.text
    
    msg = bot.send_message(user_id, "🏷️ *Qiziqishlari*\n\nQiziqishnoma yozing (vergul orqali ajrating):\nMisol: o'qish, sport, kino, sayohat")
    bot.register_next_step_handler(msg, get_interests)

def get_interests(message):
    """Qiziqishlari olish"""
    user_id = message.chat.id
    user_data[user_id]['interests'] = message.text
    
    msg = bot.send_message(
        user_id, 
        "📸 *Rasm yuklang*\n\nProfile rasmini yuklang (JPG, PNG):"
    )
    bot.register_next_step_handler(msg, get_photo)

def get_photo(message):
    """Rasm olish"""
    user_id = message.chat.id
    
    if message.photo:
        photo_id = message.photo[-1].file_id
        user_data[user_id]['photo_id'] = photo_id
        
        # Database ga saqlash
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            INSERT INTO users 
            (telegram_id, full_name, age, gender, city, bio, photo_id, interests, looking_for, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                user_data[user_id]['full_name'],
                user_data[user_id]['age'],
                user_data[user_id]['gender'],
                user_data[user_id]['city'],
                user_data[user_id]['bio'],
                photo_id,
                user_data[user_id]['interests'],
                user_data[user_id]['looking_for'],
                datetime.now()
            ))
            conn.commit()
            
            bot.send_message(
                user_id,
                "✅ *Tabriklaymiz!*\n\nProfilingiz yaratildi. Endi matching ni boshlash mumkin!",
                parse_mode="Markdown"
            )
            send_main_menu(user_id)
        except Exception as e:
            bot.send_message(user_id, f"❌ Xatolik: {str(e)}")
        finally:
            conn.close()
    else:
        msg = bot.send_message(user_id, "❌ Iltimos, rasm yuklang:")
        bot.register_next_step_handler(msg, get_photo)

# ================== MATCHING LOGIC ==================

@bot.callback_query_handler(func=lambda call: call.data == "start_matching")
def start_matching(call):
    """Matching boshlash"""
    user_id = call.message.chat.id
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (user_id,))
    current_user = cursor.fetchone()
    
    if not current_user:
        bot.send_message(user_id, "❌ Iltimos, avval profil yarating!")
        conn.close()
        return
    
    # Mosadil foydalanuvchini topish
    gender_filter = "👨 Erkak" if current_user['looking_for'] == "👩 Ayol" else "👩 Ayol" if current_user['looking_for'] == "👨 Erkak" else f"'{current_user['looking_for']}'"
    
    query = f'''
    SELECT * FROM users 
    WHERE telegram_id != ? 
    AND gender = ?
    AND telegram_id NOT IN (
        SELECT to_user_id FROM likes WHERE from_user_id = ?
    )
    LIMIT 1
    '''
    
    cursor.execute(query, (user_id, current_user['gender'], user_id))
    profile = cursor.fetchone()
    conn.close()
    
    if profile:
        show_profile_for_matching(user_id, profile)
    else:
        bot.send_message(user_id, "❌ Hozirda yangi profillar yo'q. Keyinroq qayta urinib ko'ring!")

def show_profile_for_matching(user_id, profile):
    """Profile ko'rsatish"""
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("❤️ Like", callback_data=f"like_{profile['telegram_id']}"),
        InlineKeyboardButton("👎 Reject", callback_data=f"reject_{profile['telegram_id']}")
    )
    markup.add(InlineKeyboardButton("↩️ Ortga", callback_data="back_to_menu"))
    
    profile_text = f"""
👤 *{profile['full_name']}*, {profile['age']} yosh
📍 {profile['city']}
💬 {profile['bio']}
🏷️ Qiziqishlari: {profile['interests']}
"""
    
    try:
        bot.send_photo(
            user_id,
            profile['photo_id'],
            caption=profile_text,
            reply_markup=markup,
            parse_mode="Markdown"
        )
    except:
        bot.send_message(user_id, profile_text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("like_"))
def handle_like(call):
    """Like bosilganda"""
    from_user = call.message.chat.id
    to_user = int(call.data.split("_")[1])
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Like saqlash
    cursor.execute('''
    INSERT INTO likes (from_user_id, to_user_id, action, created_at)
    VALUES (?, ?, 'like', ?)
    ''', (from_user, to_user, datetime.now()))
    
    # Tekshirish: agar to_user ham like bosgan bo'lsa, match!
    cursor.execute('''
    SELECT * FROM likes 
    WHERE from_user_id = ? AND to_user_id = ? AND action = 'like'
    ''', (to_user, from_user))
    
    if cursor.fetchone():
        # Match yaratish
        cursor.execute('''
        INSERT INTO matches (user1_id, user2_id, matched_at)
        VALUES (?, ?, ?)
        ''', (from_user, to_user, datetime.now()))
        
        conn.commit()
        conn.close()
        
        bot.send_message(from_user, "🎉 *MATCH!*\n\nSiz o'zaro like bosdingiz!\n💬 Endi suhbatlashishingiz mumkin!")
        bot.send_message(to_user, "🎉 *MATCH!*\n\nSiz o'zaro like bosdingiz!\n💬 Endi suhbatlashishingiz mumkin!", parse_mode="Markdown")
    else:
        conn.commit()
        conn.close()
        bot.send_message(from_user, "❤️ Like yuborildi!")
    
    # Keyingi profil ko'rsatish
    start_matching(call)

@bot.callback_query_handler(func=lambda call: call.data.startswith("reject_"))
def handle_reject(call):
    """Reject bosilganda"""
    from_user = call.message.chat.id
    to_user = int(call.data.split("_")[1])
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO likes (from_user_id, to_user_id, action, created_at)
    VALUES (?, ?, 'reject', ?)
    ''', (from_user, to_user, datetime.now()))
    
    conn.commit()
    conn.close()
    
    bot.send_message(from_user, "👎 Reject bo'ldi.")
    start_matching(call)

# ================== CHATS ==================

@bot.callback_query_handler(func=lambda call: call.data == "my_chats")
def my_chats(call):
    """Mening suhbatlari"""
    user_id = call.message.chat.id
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT DISTINCT 
        CASE 
            WHEN user1_id = ? THEN user2_id
            ELSE user1_id
        END as other_user_id
    FROM matches
    WHERE user1_id = ? OR user2_id = ?
    ''', (user_id, user_id, user_id))
    
    matches = cursor.fetchall()
    conn.close()
    
    if not matches:
        bot.send_message(user_id, "❌ Hali suhbatlar yo'q.")
        return
    
    markup = InlineKeyboardMarkup()
    
    for match in matches:
        other_user_id = match['other_user_id']
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT full_name FROM users WHERE telegram_id = ?", (other_user_id,))
        other_user = cursor.fetchone()
        conn.close()
        
        if other_user:
            markup.add(
                InlineKeyboardButton(
                    other_user['full_name'],
                    callback_data=f"open_chat_{other_user_id}"
                )
            )
    
    markup.add(InlineKeyboardButton("↩️ Ortga", callback_data="back_to_menu"))
    bot.send_message(user_id, "💬 *Mening Suhbatlarim*", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("open_chat_"))
def open_chat(call):
    """Chat ochish"""
    user_id = call.message.chat.id
    other_user_id = int(call.data.split("_")[2])
    
    # Chat history yuklash
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM messages 
    WHERE (from_user_id = ? AND to_user_id = ?)
    OR (from_user_id = ? AND to_user_id = ?)
    ORDER BY created_at DESC
    LIMIT 10
    ''', (user_id, other_user_id, other_user_id, user_id))
    
    messages = cursor.fetchall()
    conn.close()
    
    if messages:
        chat_text = "📜 *So'nggi suhbatlar:*\n\n"
        for msg in reversed(messages):
            sender = "Siz" if msg['from_user_id'] == user_id else "Ular"
            chat_text += f"{sender}: {msg['message']}\n"
    else:
        chat_text = "Hali suhbat yo'q. Boshlang!"
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📝 Xabar yozing", callback_data=f"write_msg_{other_user_id}"))
    markup.add(InlineKeyboardButton("↩️ Ortga", callback_data="my_chats"))
    
    bot.send_message(user_id, chat_text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("write_msg_"))
def write_message(call):
    """Xabar yozish"""
    user_id = call.message.chat.id
    other_user_id = int(call.data.split("_")[2])
    
    user_data[user_id] = {'chat_with': other_user_id}
    
    msg = bot.send_message(user_id, "📝 Xabaringizni yozing:")
    bot.register_next_step_handler(msg, send_message)

def send_message(message):
    """Xabar yuborish"""
    user_id = message.chat.id
    other_user_id = user_data[user_id]['chat_with']
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Match ID ni topish
    cursor.execute('''
    SELECT id FROM matches
    WHERE (user1_id = ? AND user2_id = ?) OR (user1_id = ? AND user2_id = ?)
    ''', (user_id, other_user_id, other_user_id, user_id))
    
    match = cursor.fetchone()
    
    if match:
        cursor.execute('''
        INSERT INTO messages (match_id, from_user_id, to_user_id, message, created_at)
        VALUES (?, ?, ?, ?, ?)
        ''', (match['id'], user_id, other_user_id, message.text, datetime.now()))
        
        conn.commit()
        conn.close()
        
        bot.send_message(user_id, "✅ Xabar yuborildi!")
        bot.send_message(other_user_id, f"💬 Yangi xabar!\n\n{message.text}")
    else:
        conn.close()
        bot.send_message(user_id, "❌ Xatolik yuz berdi.")

# ================== PROFILE ==================

@bot.callback_query_handler(func=lambda call: call.data == "view_profile")
def view_profile(call):
    """Profil ko'rish"""
    user_id = call.message.chat.id
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        profile_text = f"""
👤 *{user['full_name']}*
🎂 Yosh: {user['age']}
👥 Jinsiy xususiyat: {user['gender']}
📍 Shahar: {user['city']}
💬 Bio: {user['bio']}
🏷️ Qiziqishlari: {user['interests']}
🔍 Izlayotgan: {user['looking_for']}
"""
        
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("✏️ O'zgartirish", callback_data="edit_profile"))
        markup.add(InlineKeyboardButton("↩️ Ortga", callback_data="back_to_menu"))
        
        try:
            bot.send_photo(
                user_id,
                user['photo_id'],
                caption=profile_text,
                reply_markup=markup,
                parse_mode="Markdown"
            )
        except:
            bot.send_message(user_id, profile_text, reply_markup=markup, parse_mode="Markdown")
    else:
        bot.send_message(user_id, "❌ Profil topilmadi.")

# ================== UTILITY ==================

@bot.callback_query_handler(func=lambda call: call.data == "back_to_menu")
def back_to_menu(call):
    """Asosiy menuga qaytish"""
    send_main_menu(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "help")
def help_handler(call):
    """Qo'llanma"""
    help_text = """
🌹 *Sara Match Qo'llanmasi*

*Qanday ishlaydi?*
1️⃣ Profile yarating
2️⃣ Boshqa foydalanuvchilarni ko'ring
3️⃣ Like yoki Reject bosing
4️⃣ Agar ikkalasi ham like bosdi - MATCH!
5️⃣ Suhbatlashing va do'stlarni toping

*Buttons:*
❤️ Like - Shaxs sizga yoqdi
👎 Reject - Shaxs sizga yoqmadi
💬 Suhbatlar - Mached users bilan suhbat
👤 Profilim - O'zingizni ko'rish

*Tips:*
✨ To'liq profile - ko'proq matches!
📸 Yoqimli rasm qo'ying
💬 Qiziq bio yozing
"""
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("↩️ Ortga", callback_data="back_to_menu"))
    
    bot.send_message(call.message.chat.id, help_text, reply_markup=markup, parse_mode="Markdown")

if __name__ == "__main__":
    print("🤖 Sara Match Bot ishga tushdi...")
    init_db()
    bot.infinity_polling()
