import sqlite3
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = 33422392 
API_HASH = "9b66ed5b9e6a307951b3a681c80f9d4b"
BOT_TOKEN = "8651064244:AAEdUCZRl-nYcz-TRrkhhSDbMV1v8jUUk5w"
OWNER_USERNAME = "CYBER_71_ENAFUL" 
ADMIN_ID = 6823368645 
app = Client("app_storage_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

db = sqlite3.connect("bot_data.db", check_same_thread=False)
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)")
cursor.execute("CREATE TABLE IF NOT EXISTS apps (file_id TEXT, file_name TEXT)")
db.commit()

def get_apps_keyboard():
    cursor.execute("SELECT file_id, file_name FROM apps")
    all_apps = cursor.fetchall()
    buttons = []
    for fid, name in all_apps:
        buttons.append([InlineKeyboardButton(f"📥 {name} 📱", callback_data=f"get_{fid[:15]}")])
    return InlineKeyboardMarkup(buttons)

@app.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    cursor.execute("INSERT OR IGNORE INTO users VALUES (?)", (user_id,))
    db.commit()
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("👨‍💻 বোটের মালিক (Contact) 📱", url=f"https://t.me/{OWNER_USERNAME}")],
        [InlineKeyboardButton("📂 সব অ্যাপ দেখুন 📱", callback_data="show_apps")],
        [InlineKeyboardButton("📊 আমার স্ট্যাটাস 📱", callback_data="my_stats")]
    ])
    
    welcome_text = (
        f"👋 **স্বাগতম!**\n\n"
        f"বোটের বর্তমান অবস্থা এবং তথ্যের তালিকা নিচে দেওয়া হলো:\n\n"
        f"👤 **নাম:** {message.from_user.first_name}\n"
        f"🆔 **আইডি:** `{user_id}`\n"
        f"🛠 **ডেভেলপার:** @{OWNER_USERNAME}\n\n"
        f"নিচের বাটনগুলো ব্যবহার করে ফাইলগুলো চেক করুন। 📱"
    )
    await message.reply_text(welcome_text, reply_markup=keyboard)

@app.on_message(filters.document)
async def store_apps(client, message):
    if message.document.file_name.endswith(".apk"):
        file_id = message.document.file_id
        file_name = message.document.file_name
        cursor.execute("INSERT INTO apps VALUES (?, ?)", (file_id, file_name))
        db.commit()
        
        del_btn = None
        if message.from_user.id == ADMIN_ID:
            del_btn = InlineKeyboardMarkup([[InlineKeyboardButton(f"🗑 Delete {file_name} 📱", callback_data=f"del_{file_id[:15]}") ]])
        
        await message.reply_text(f"✅ **'{file_name}'** সেভ হয়েছে! এটি এখন অটো-মেনুতে দেখা যাবে। 📱", reply_markup=del_btn)
    else:
        await message.reply_text("❌ শুধুমাত্র APK ফাইল পাঠান। 📱")

@app.on_callback_query()
async def callback_handler(client, query):
    data = query.data
    
    if data == "show_apps":
        keyboard = get_apps_keyboard()
        if not keyboard.inline_keyboard:
            await query.message.edit_text("📭 বর্তমানে স্টোরেজে কোনো অ্যাপ নেই! 📱", 
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ব্যাকে যান 📱", callback_data="back_to_start")]]))
        else:
            await query.message.edit_text("📱 **স্টোরে থাকা সব অ্যাপের লিস্ট:**", reply_markup=keyboard)

    elif data == "my_stats":
        await query.answer(f"আপনার আইডি: {query.from_user.id} 📱", show_alert=True)

    elif data == "back_to_start":
        await start(client, query.message)

    elif data.startswith("get_"):
        short_id = data.split("_")[1]
        cursor.execute("SELECT file_id FROM apps")
        all_f = cursor.fetchall()
        for f in all_f:
            if f[0].startswith(short_id):
                await query.message.reply_document(f[0])
                await query.answer("ফাইলটি পাঠানো হচ্ছে... 📱")
                break

    elif data.startswith("del_") and query.from_user.id == ADMIN_ID:
        short_id = data.split("_")[1]
        cursor.execute("DELETE FROM apps WHERE file_id LIKE ?", (short_id + "%",))
        db.commit()
        await query.message.edit_text("🗑 ফাইলটি রিমুভ করা হয়েছে। 📱")

@app.on_message(filters.command("admin") & filters.user(ADMIN_ID))
async def admin_panel(client, message):
    cursor.execute("SELECT COUNT(*) FROM users")
    u_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM apps")
    a_count = cursor.fetchone()[0]
    
    text = f"📊 **বোট পরিসংখ্যান:**\n\n👤 মোট ইউজার: {u_count}\n📦 মোট অ্যাপ সেভড: {a_count} 📱"
    await message.reply_text(text)

print("বোটটি সফলভাবে চালু হয়েছে... 📱")
app.run()

