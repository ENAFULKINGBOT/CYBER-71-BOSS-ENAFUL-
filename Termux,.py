import sqlite3
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply

API_ID = "21609142" 
API_HASH = "699bb01ac7873fabc7212db10dc9ffdc" 
BOT_TOKEN = "7708154020:AAEhKUFfVh2KZeUIl1uT7Cnn43wYODyaFis"

ADMIN_USERNAME = "CYBER_71_ENAFUL" 
APP_PASSWORD = "KING OF ENAFUL" 
MY_ID_LINK = "https://t.me/KING_OF_ENAFUL"
MY_ID_NAME = "@KING_OF_ENAFUL"

app = Client("PremiumStore_Bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def init_db():
    conn = sqlite3.connect("apps_store.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS apps (name TEXT, file_id TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER UNIQUE)")
    conn.commit()
    conn.close()

init_db()

def add_user(user_id):
    conn = sqlite3.connect("apps_store.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

@app.on_message(filters.command("start"))
async def start(client, message):
    add_user(message.from_user.id)
    
    conn = sqlite3.connect("apps_store.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM apps")
    rows = cursor.fetchall()
    conn.close()

    welcome_text = (
        f"┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        f"┃   🚀 **PREMIUM APP STORE** ┃\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
        f"👋 **Welcome Mr. {message.from_user.first_name}!**\n"
        f"👤 **Admin:** {MY_ID_NAME}\n\n"
        f"এটি একটি সিকিউর অ্যাপ ডিস্ট্রিবিউশন প্ল্যাটফর্ম।\n\n"
        f"📢 **বট স্ট্যাটাস:**\n"
        f"┣ 📦 **মোট অ্যাপ:** {len(rows)} টি\n"
        f"┗ 🔐 **সিকিউরিটি:** পাসওয়ার্ড প্রোটেক্টেড\n\n"
        f"⚠️ **নির্দেশনা:** নিচের বাটন থেকে অ্যাপ সিলেক্ট করুন এবং পাসওয়ার্ড দিয়ে ডাউনলোড করুন।"
    )

    keyboard = []
    for i in range(len(rows)):
        app_name = rows[i][0]
        keyboard.append([InlineKeyboardButton(f"{app_name}", callback_data=f"ask_pw_{i}")])
    
    keyboard.append([InlineKeyboardButton("➖➖➖➖➖➖➖➖➖➖", callback_data="none")])
    keyboard.append([InlineKeyboardButton(f"👨‍💻 Contact Admin: {MY_ID_NAME}", url=MY_ID_LINK)])

    await message.reply_text(text=welcome_text, reply_markup=InlineKeyboardMarkup(keyboard))

@app.on_message(filters.command("all") & filters.user(ADMIN_USERNAME))
async def broadcast(client, message):
    if len(message.command) < 2:
        await message.reply_text("❌ ব্যবহার বিধি: `/all মেসেজ`")
        return
    msg_to_send = message.text.split(None, 1)[1]
    conn = sqlite3.connect("apps_store.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    conn.close()
    
    await message.reply_text("🚀 ব্রডকাস্টিং শুরু হয়েছে...")
    count = 0
    for user in users:
        try:
            await client.send_message(user[0], f"📢 **নতুন নোটিশ:**\n\n{msg_to_send}")
            count += 1
        except: pass
    await message.reply_text(f"✅ সফলভাবে {count} জন ইউজারের কাছে পাঠানো হয়েছে।")
@app.on_callback_query(filters.regex(r"ask_pw_(\d+)"))
async def ask_password(client, query):
    index = query.data.split("_")[2]
    await query.message.reply_text(
        f"🔑 **পাসওয়ার্ড ভেরিফিকেশন:**\nফাইলের আইডি: `{index}`\n\nএই মেসেজটিতে রিপ্লাই দিয়ে পাসওয়ার্ডটি লিখুন।\nপাসওয়ার্ড পেতে {MY_ID_NAME}-এ মেসেজ দিন।",
        reply_markup=ForceReply(selective=True)
    )

@app.on_message(filters.reply & ~filters.command(["start", "all"]))
async def check_password(client, message):
    if message.reply_to_message and "🔑 পাসওয়ার্ড ভেরিফিকেশন" in message.reply_to_message.text:
        if message.text.strip() == APP_PASSWORD:
            try:
                index = int(message.reply_to_message.text.split("`")[1])
                conn = sqlite3.connect("apps_store.db")
                cursor = conn.cursor()
                cursor.execute("SELECT name, file_id FROM apps")
                rows = cursor.fetchall()
                conn.close()
                name, file_id = rows[index]
                await message.reply_document(file_id, caption=f"🚀 **{name}**\n✅ ভেরিফাইড ইউজার।\n👨‍💻 Admin: {MY_ID_NAME}")
            except:
                await message.reply_text("❌ ত্রুটি হয়েছে!")
        else:
            await message.reply_text(f"🚫 পাসওয়ার্ড ভুল!")

@app.on_message(filters.document & filters.user(ADMIN_USERNAME))
async def auto_save_app(client, message):
    file_name = f"📱 {message.document.file_name}"
    file_id = message.document.file_id
    conn = sqlite3.connect("apps_store.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO apps (name, file_id) VALUES (?, ?)", (file_name, file_id))
    conn.commit()
    conn.close()
    await message.reply_text(f"✅ অ্যাপ স্টোরে যুক্ত হয়েছে: `{file_name}`")

print("বটটি নতুন API HASH সহ অনলাইনে আছে...")
app.run()

