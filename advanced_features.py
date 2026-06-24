# Sara Match Bot - Advanced Features Module

"""
Bu file sara_match_bot.py ga qo'sh qilib ishlatiladi
Admin panel, statistika va advanced features uchun
"""

import sqlite3
from datetime import datetime, timedelta
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ================== ADMIN PANEL ==================

ADMIN_IDS = [YOUR_TELEGRAM_ID]  # Shu yerga o'zingizning ID sini qo'ying

def is_admin(user_id):
    """Admin ekanligini tekshirish"""
    return user_id in ADMIN_IDS

def register_admin_handlers(bot):
    """Admin handlerlari registratsiya qilish"""
    
    @bot.message_handler(commands=['admin'])
    def admin_panel(message):
        user_id = message.chat.id
        if not is_admin(user_id):
            bot.send_message(user_id, "❌ Sizda ruxsat yo'q!")
            return
        
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("📊 Statistika", callback_data="admin_stats"),
            InlineKeyboardButton("👥 Foydalanuvchilar", callback_data="admin_users")
        )
        markup.add(
            InlineKeyboardButton("⚠️ Reportlar", callback_data="admin_reports"),
            InlineKeyboardButton("📢 Xabar yubor", callback_data="admin_broadcast")
        )
        
        bot.send_message(user_id, "🔐 *Admin Panel*", reply_markup=markup, parse_mode="Markdown")
    
    @bot.callback_query_handler(func=lambda call: call.data == "admin_stats")
    def show_stats(call):
        if not is_admin(call.message.chat.id):
            return
        
        stats = get_statistics()
        
        stats_text = f"""
📊 *STATISTIKA*

👥 Jami Foydalanuvchilar: {stats['total_users']}
👨 Erkaklar: {stats['male_users']}
👩 Ayollar: {stats['female_users']}

💕 Jami Liklar: {stats['total_likes']}
🎉 Jami Matchlar: {stats['total_matches']}
💬 Jami Xabarlar: {stats['total_messages']}

📈 Bugun yangi: {stats['new_today']}
🔄 Bugun Liklar: {stats['likes_today']}

⏰ So'ngi update: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
        
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("↩️ Ortga", callback_data="admin_back"))
        
        bot.send_message(call.message.chat.id, stats_text, reply_markup=markup, parse_mode="Markdown")
    
    @bot.callback_query_handler(func=lambda call: call.data == "admin_users")
    def show_users(call):
        if not is_admin(call.message.chat.id):
            return
        
        conn = sqlite3.connect('sara_match.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT telegram_id, full_name, age, gender, city, created_at FROM users ORDER BY created_at DESC LIMIT 20")
        users = cursor.fetchall()
        conn.close()
        
        users_text = "*👥 So'ngi 20 Foydalanuvchi*\n\n"
        for user in users:
            users_text += f"• {user[1]} ({user[2]} yosh) - {user[3]}\n"
            users_text += f"  📍 {user[4]} | ID: {user[0]}\n"
        
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("↩️ Ortga", callback_data="admin_back"))
        
        bot.send_message(call.message.chat.id, users_text, reply_markup=markup, parse_mode="Markdown")
    
    @bot.callback_query_handler(func=lambda call: call.data == "admin_broadcast")
    def broadcast_message(call):
        if not is_admin(call.message.chat.id):
            return
        
        msg = bot.send_message(call.message.chat.id, "📢 Barcha foydalanuvchilarga yuboriladigan xabari kiriting:")
        bot.register_next_step_handler(msg, lambda m: do_broadcast(bot, call.message.chat.id, m))
    
    def do_broadcast(bot, admin_id, message):
        """Barcha foydalanuvchilarga xabar yuborish"""
        conn = sqlite3.connect('sara_match.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT telegram_id FROM users")
        users = cursor.fetchall()
        conn.close()
        
        count = 0
        for user in users:
            try:
                bot.send_message(user[0], message.text)
                count += 1
            except:
                pass
        
        bot.send_message(admin_id, f"✅ {count} ta foydalanuvchiga xabar yuborildi!")

# ================== STATISTIKA FUNKSIYALARI ==================

def get_statistics():
    """Asosiy statistikani olish"""
    conn = sqlite3.connect('sara_match.db')
    cursor = conn.cursor()
    
    # Jami foydalanuvchilar
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    
    # Erkaklar va ayollar
    cursor.execute("SELECT COUNT(*) FROM users WHERE gender LIKE '%Erkak%'")
    male = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM users WHERE gender LIKE '%Ayol%'")
    female = cursor.fetchone()[0]
    
    # Liklar
    cursor.execute("SELECT COUNT(*) FROM likes WHERE action = 'like'")
    total_likes = cursor.fetchone()[0]
    
    # Matchlar
    cursor.execute("SELECT COUNT(*) FROM matches")
    total_matches = cursor.fetchone()[0]
    
    # Xabarlar
    cursor.execute("SELECT COUNT(*) FROM messages")
    total_messages = cursor.fetchone()[0]
    
    # Bugun yangi foydalanuvchilar
    today = datetime.now().date()
    cursor.execute("SELECT COUNT(*) FROM users WHERE DATE(created_at) = ?", (today,))
    new_today = cursor.fetchone()[0]
    
    # Bugun liklar
    cursor.execute("SELECT COUNT(*) FROM likes WHERE DATE(created_at) = ? AND action = 'like'", (today,))
    likes_today = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'total_users': total_users,
        'male_users': male,
        'female_users': female,
        'total_likes': total_likes,
        'total_matches': total_matches,
        'total_messages': total_messages,
        'new_today': new_today,
        'likes_today': likes_today
    }

# ================== ADVANCED FILTERING ==================

def get_filtered_profiles(user_id, age_min=18, age_max=80, distance_km=None):
    """Advanced filtering bilan profillar olish"""
    conn = sqlite3.connect('sara_match.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (user_id,))
    current_user = cursor.fetchone()
    
    if not current_user:
        return None
    
    # Query yasash
    query = '''
    SELECT * FROM users 
    WHERE telegram_id != ? 
    AND age BETWEEN ? AND ?
    AND telegram_id NOT IN (
        SELECT to_user_id FROM likes WHERE from_user_id = ?
    )
    '''
    
    params = [user_id, age_min, age_max, user_id]
    
    # Optional: Shahar filteri
    if current_user['looking_for'] != "Farqi yo'q":
        query += " AND gender = ?"
        params.append(current_user['looking_for'])
    
    cursor.execute(query, params)
    profiles = cursor.fetchall()
    conn.close()
    
    return profiles

# ================== REPORT & BAN SYSTEM ==================

def create_report(from_user_id, to_user_id, reason):
    """Report yaratish"""
    conn = sqlite3.connect('sara_match.db')
    cursor = conn.cursor()
    
    # Reports table yaratish
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY,
        from_user_id INTEGER,
        to_user_id INTEGER,
        reason TEXT,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP
    )
    ''')
    
    cursor.execute('''
    INSERT INTO reports (from_user_id, to_user_id, reason, created_at)
    VALUES (?, ?, ?, ?)
    ''', (from_user_id, to_user_id, reason, datetime.now()))
    
    conn.commit()
    conn.close()

def ban_user(user_id, reason=""):
    """Foydalanuvchini bloklasch"""
    conn = sqlite3.connect('sara_match.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE users 
    SET status = 'banned' 
    WHERE telegram_id = ?
    ''', (user_id,))
    
    conn.commit()
    conn.close()

def is_banned(user_id):
    """Foydalanuvchi blocked ekanligini tekshirish"""
    conn = sqlite3.connect('sara_match.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT status FROM users WHERE telegram_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    return result and result[0] == 'banned'

# ================== PROFILE COMPLETION SCORE ==================

def get_profile_score(user_id):
    """Profile % ni hisoblash"""
    conn = sqlite3.connect('sara_match.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return 0
    
    score = 0
    
    if user['full_name']: score += 20
    if user['age']: score += 15
    if user['gender']: score += 15
    if user['city']: score += 15
    if user['bio'] and len(user['bio']) > 10: score += 15
    if user['photo_id']: score += 20
    
    return min(score, 100)

# ================== MATCHING ANALYTICS ==================

def get_user_matches_stats(user_id):
    """Foydalanuvchining match statistikasi"""
    conn = sqlite3.connect('sara_match.db')
    cursor = conn.cursor()
    
    # Yuborgan liklar
    cursor.execute("SELECT COUNT(*) FROM likes WHERE from_user_id = ? AND action = 'like'", (user_id,))
    sent_likes = cursor.fetchone()[0]
    
    # Olgan liklar
    cursor.execute("SELECT COUNT(*) FROM likes WHERE to_user_id = ? AND action = 'like'", (user_id,))
    received_likes = cursor.fetchone()[0]
    
    # Matchlar
    cursor.execute("SELECT COUNT(*) FROM matches WHERE user1_id = ? OR user2_id = ?", (user_id, user_id))
    matches = cursor.fetchone()[0]
    
    # So'ngi match
    cursor.execute('''
    SELECT matched_at FROM matches 
    WHERE user1_id = ? OR user2_id = ?
    ORDER BY matched_at DESC LIMIT 1
    ''', (user_id, user_id))
    
    last_match = cursor.fetchone()
    
    conn.close()
    
    return {
        'sent_likes': sent_likes,
        'received_likes': received_likes,
        'total_matches': matches,
        'last_match': last_match[0] if last_match else None,
        'match_rate': (received_likes / max(sent_likes, 1)) * 100 if sent_likes > 0 else 0
    }

# ================== NOTIFICATIONS ==================

def send_daily_reminder(bot, user_id):
    """Kunlik reminder yuborish"""
    conn = sqlite3.connect('sara_match.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM likes WHERE to_user_id = ? AND action = 'like'", (user_id,))
    new_likes = cursor.fetchone()[0]
    
    conn.close()
    
    if new_likes > 0:
        text = f"🔔 *Kunlik Reminder*\n\nSizga {new_likes} ta yangi like bor! 💕\n\n/start bosib ko'ring!"
        try:
            bot.send_message(user_id, text, parse_mode="Markdown")
        except:
            pass

# ================== VERIFICATION ==================

def require_email_verification(user_id, email):
    """Email verification (optional)"""
    conn = sqlite3.connect('sara_match.db')
    cursor = conn.cursor()
    
    # Email verification table yaratish
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS email_verification (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        email TEXT,
        token TEXT,
        verified BOOLEAN DEFAULT 0,
        created_at TIMESTAMP
    )
    ''')
    
    # Random token yaratish
    import uuid
    token = str(uuid.uuid4())
    
    cursor.execute('''
    INSERT INTO email_verification (user_id, email, token, created_at)
    VALUES (?, ?, ?, ?)
    ''', (user_id, email, token, datetime.now()))
    
    conn.commit()
    conn.close()
    
    return token

# ================== USAGE EXAMPLE ==================

"""
sara_match_bot.py ga qo'shing:

from advanced_features import (
    register_admin_handlers,
    get_statistics,
    is_banned,
    get_profile_score,
    get_user_matches_stats
)

# Main kodda:
register_admin_handlers(bot)

# Profile kiritishdan oldin:
if is_banned(user_id):
    bot.send_message(user_id, "❌ Sizning akkauntingiz blocked!")
    return

# Profile ko'rish uchun:
score = get_profile_score(user_id)
stats = get_user_matches_stats(user_id)
"""
