import telebot
from telebot import types
import os
import time


API_TOKEN = '8714968781:AAHO8Z3JIXkh4swijmFtg2G5_wTdhj59F3c'
ADMIN_ID = 6823368645  
ADMIN_USERNAME = "@KING_OF_ENAFUL"
bot = telebot.TeleBot(API_TOKEN)
USER_FILE = "users.txt"

if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f: pass

def get_users():
    with open(USER_FILE, "r") as f:
        return f.read().splitlines()

def add_user(user_id):
    users = get_users()
    if str(user_id) not in users:
        with open(USER_FILE, "a") as f:
            f.write(str(user_id) + "\n")

def remove_user_from_db(user_id):
    users = get_users()
    if str(user_id) in users:
        users.remove(str(user_id))
        with open(USER_FILE, "w") as f:
            for u in users:
                f.write(u + "\n")
        return True
    return False

def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item1 = types.KeyboardButton('📤 Broadcast APK/File')
    item2 = types.KeyboardButton('📊 Full Stats')
    item3 = types.KeyboardButton('🛠 Admin Tools')
    item4 = types.KeyboardButton('💬 Contact Admin')
    item5 = types.KeyboardButton('ℹ️ About Bot')
    markup.add(item1, item2, item3, item4, item5)
    return markup

def admin_tools_menu():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item1 = types.KeyboardButton('🗑 Remove User ID')
    item2 = types.KeyboardButton('🧹 Clear All Users')
    item3 = types.KeyboardButton('🔙 Back to Main Menu')
    markup.add(item1, item2, item3)
    return markup

def cancel_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('❌ Cancel'))
    return markup
@bot.message_handler(commands=['start'])
def start(message):
    add_user(message.chat.id)
    welcome_text = (
        "✨ **BOSS ENAFUL ব্রডকাস্ট বটে স্বাগতম!** ✨\n\n"
        "✅ **সরাসরি ব্রডকাস্ট:** অ্যাডমিন কোনো টেক্সট লিখলে তা সরাসরি সবার কাছে যাবে।\n"
        "📦 **ফাইল ব্রডকাস্ট:** বাটন ব্যবহার করে APK বা ফাইল পাঠান।\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "👇 নিচের মেনু বাটনগুলো ব্যবহার করুন:"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown', reply_markup=main_menu())

@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    if message.chat.id == ADMIN_ID:
        if message.text == '📊 Full Stats':
            users = get_users()
            bot.reply_to(message, f"👥 **বট স্ট্যাটাস:**\n\nমোট ইউজার: {len(users)}\nস্ট্যাটাস: একটিভ ✅", parse_mode='Markdown')

        elif message.text == '📤 Broadcast APK/File':
            msg = bot.send_message(message.chat.id, "📁 যেকোনো APK বা ফাইল পাঠান।", reply_markup=cancel_menu())
            bot.register_next_step_handler(msg, start_broadcasting)

        elif message.text == '🛠 Admin Tools':
            bot.reply_to(message, "⚙️ অ্যাডমিন টুলস ওপেন হয়েছে:", reply_markup=admin_tools_menu())

        elif message.text == '🗑 Remove User ID':
            msg = bot.send_message(message.chat.id, "রিমুভ করতে আইডিটি দিন:", reply_markup=cancel_menu())
            bot.register_next_step_handler(msg, process_remove_user)

        elif message.text == '🧹 Clear All Users':
            with open(USER_FILE, "w") as f: pass
            bot.reply_to(message, "✅ ডাটাবেস সম্পূর্ণ ক্লিয়ার করা হয়েছে।")

        elif message.text == '🔙 Back to Main Menu':
            bot.reply_to(message, "প্রধান মেনু:", reply_markup=main_menu())

        elif message.text not in ['📊 Full Stats', '📤 Broadcast APK/File', '🛠 Admin Tools', '💬 Contact Admin', 'ℹ️ About Bot', '🗑 Remove User ID', '🧹 Clear All Users', '🔙 Back to Main Menu']:
            users = get_users()
            success = 0
            for user in users:
                try:
                    bot.send_message(user, message.text)
                    success += 1
                except: continue
            bot.send_message(ADMIN_ID, f"✅ সরাসরি টেক্সট ব্রডকাস্ট সম্পন্ন!\n📤 সফল: {success} জন।")

    if message.text == '💬 Contact Admin':
        bot.reply_to(message, f"👨‍💻 অ্যাডমিনের সাথে যোগাযোগ করুন: {ADMIN_USERNAME}")
    
    elif message.text == 'ℹ️ About Bot':
        about_msg = (
            f"🤖 **Cyber 71 Enaful Assistant**\n\n"
            f"👤 **মালিক:** BOSS ENAFUL\n"
            f"🔗 **ইউজারনেম:** {ADMIN_USERNAME}\n"
            f"🛠 **প্ল্যাটফর্ম:** Termux (Python)"
        )
        bot.reply_to(message, about_msg, parse_mode='Markdown')

def start_broadcasting(message):
    if message.text == '❌ Cancel':
        bot.send_message(ADMIN_ID, "🚫 ব্রডকাস্ট বাতিল।", reply_markup=main_menu())
        return

    users = get_users()
    success = 0
    bot.send_message(ADMIN_ID, "🚀 ফাইল ব্রডকাস্টিং শুরু হয়েছে...")

    for user in users:
        try:
            if message.content_type == 'document':
                bot.send_document(user, message.document.file_id, caption=message.caption)
            elif message.content_type == 'photo':
                bot.send_photo(user, message.photo[-1].file_id, caption=message.caption)
            elif message.content_type == 'video':
                bot.send_video(user, message.video.file_id, caption=message.caption)
            elif message.content_type == 'text':
                bot.send_message(user, message.text)
            success += 1
        except: continue
            
    bot.send_message(ADMIN_ID, f"✅ ফাইল ব্রডকাস্ট সম্পন্ন!\n📤 সফল: {success} জন।", reply_markup=main_menu())

def process_remove_user(message):
    if message.text == '❌ Cancel':
        bot.send_message(ADMIN_ID, "বাতিল করা হয়েছে।", reply_markup=admin_tools_menu())
        return
    if remove_user_from_db(message.text):
        bot.reply_to(message, f"✅ ইউজার {message.text} কে রিমুভ করা হয়েছে।", reply_markup=admin_tools_menu())
    else:
        bot.reply_to(message, "❌ আইডিটি পাওয়া যায়নি।", reply_markup=admin_tools_menu())

while True:
    try:
        print(f"বট চলছে (Owner: {ADMIN_USERNAME})...")
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        time.sleep(5)

