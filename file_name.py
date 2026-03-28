import telebot
import requests
import os
from telebot import types

TOKEN = '8636376006:AAGOVtZcEcRIpPm71u-SRm5YUFHkRBhItsI'
ADMIN_USERNAME = 'KING_OF_ENAFUL' 
MY_NAME = "ENAFUL"
bot = telebot.TeleBot(TOKEN)

DB_FILE = "enaful_users.txt"
DETAILS_FILE = "user_details.txt"

def save_user(message):
    user_id = str(message.from_user.id)
    first_name = message.from_user.first_name
    username = f"@{message.from_user.username}" if message.from_user.username else "No Username"
    
    if not os.path.exists(DB_FILE):
        open(DB_FILE, "w").close()
    if not os.path.exists(DETAILS_FILE):
        open(DETAILS_FILE, "w").close()
            
    with open(DB_FILE, "r") as f:
        users = f.read()
    
    if user_id not in users:
        with open(DB_FILE, "a") as f:
            f.write(f"{user_id}\n")
        with open(DETAILS_FILE, "a") as f:
            f.write(f"🆔 ID: {user_id} | 👤 Name: {first_name} | 🔗 User: {username}\n")

def show_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("\033[1;36m")
    print(f"╔════════════════════════════════════════╗")
    print(f"║       DEVELOPER: BOSS {MY_NAME: <15}  ║")
    print(f"║       SYSTEM: JARVIS IP TRACKER v2.0   ║")
    print(f"║       ADMIN: @{ADMIN_USERNAME: <18} ║")
    print(f"║       STATUS: ONLINE & SECURE          ║")
    print(f"╚════════════════════════════════════════╝")
    print("\033[0m")

def get_location_info(ip):
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,country,countryCode,regionName,city,isp,lat,lon,query"
        return requests.get(url).json()
    except:
        return None

def main_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton("📍 আমার নিজের IP")
    btn2 = types.KeyboardButton("🛠 বটের কাজ কি?")
    btn3 = types.KeyboardButton("❓ সাহায্য")
    markup.add(btn1, btn2, btn3)
    
    if message.from_user.username == ADMIN_USERNAME:
        btn4 = types.KeyboardButton("📊 অ্যাডমিন প্যানেল")
        markup.add(btn4)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    save_user(message)
    welcome_msg = (
        f"╭══════════════ [ WELCOME ] ══════════════╮\n"
        f"   👋 আসসালামু আলাইকুম, {message.from_user.first_name}!\n"
        f"╰════════════════════════════════════════╯\n\n"
        f"আমি **Jarvis**, আপনার ব্যক্তিগত ট্র্যাকিং অ্যাসিস্ট্যান্ট।\n"
        f"এই টুলসটি তৈরি করেছেন আপনার প্রিয় **BOSS {MY_NAME}**।\n\n"
        f"✨ আপনার প্রয়োজনীয় অপশনটি নিচের মেনু থেকে সিলেক্ট করুন অথবা সরাসরি IP পাঠান।"
    )
    bot.reply_to(message, welcome_msg, parse_mode="Markdown", reply_markup=main_menu(message))

@bot.message_handler(func=lambda message: message.text == "🛠 বটের কাজ কি?")
def bot_works(message):
    works = (
        f"┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        f"     🤖 বটের প্রধান কাজসমূহ (By {MY_NAME})\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
        f"✅ **IP Tracking:** যেকোনো আইপি দিয়ে তার লোকেশন বের করা।\n"
        f"✅ **Live Map:** সরাসরি গুগল ম্যাপে অবস্থান দেখা।\n"
        f"✅ **Self Tracking:** আপনার নিজের আইপি চেক করা।\n"
        f"✅ **Admin Control:** বটের ইউজার লিস্ট ও নোটিশ পাঠানো।"
    )
    bot.reply_to(message, works, parse_mode="Markdown")

# --- অ্যাডমিন প্যানেল ও ব্রডকাস্টিং ---
@bot.message_handler(func=lambda message: message.text == "📊 অ্যাডমিন প্যানেল")
def admin_panel(message):
    if message.from_user.username == ADMIN_USERNAME:
        with open(DB_FILE, "r") as f:
            total = len(f.readlines())
        
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("📜 ইউজার লিস্ট", callback_data="show_list")
        btn2 = types.InlineKeyboardButton("📢 ব্রডকাস্টিং", callback_data="broadcast")
        markup.add(btn1, btn2)
        
        bot.reply_to(message, f"╭━━━━━━━ [ ADMIN PANEL ] ━━━━━━━╮\n\n"
                             f"   👑 BOSS: {MY_NAME}\n"
                             f"   📈 মোট ইউজার: {total} জন\n\n"
                             f"╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯", 
                     parse_mode="Markdown", reply_markup=markup)
    else:
        bot.reply_to(message, "❌ আপনি এই বটের অ্যাডমিন নন!")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "show_list":
        if os.path.exists(DETAILS_FILE):
            with open(DETAILS_FILE, "r") as f:
                data = f.read()
            if data:
                bot.send_message(call.message.chat.id, f"👥 **ইউজার লিস্ট:**\n\n{data}")
            else:
                bot.answer_callback_query(call.id, "এখনও কোনো ডাটা নেই!")
        else:
            bot.answer_callback_query(call.id, "ফাইল পাওয়া যায়নি!")
    
    elif call.data == "broadcast":
        msg = bot.send_message(call.message.chat.id, "📢 আপনার মেসেজটি লিখুন যা সবাইকে পাঠাতে চান:")
        bot.register_next_step_handler(msg, send_broadcast)

def send_broadcast(message):
    with open(DB_FILE, "r") as f:
        users = f.readlines()
    
    count = 0
    for user in users:
        try:
            bot.send_message(user.strip(), f"📢 **[ADMIN MESSAGE FROM {MY_NAME}]**\n\n{message.text}")
            count += 1
        except:
            pass
    bot.reply_to(message, f"✅ সফলভাবে {count} জন ইউজারের কাছে মেসেজ পাঠানো হয়েছে।")

@bot.message_handler(func=lambda message: message.text == "📍 আমার নিজের IP")
def my_ip(message):
    try:
        ip = requests.get('https://api.ipify.org').text
        process_ip(message, ip)
    except:
        bot.reply_to(message, "⚠️ আইপি ডিটেক্ট করতে সমস্যা হচ্ছে।")

@bot.message_handler(func=lambda message: message.text == "❓ সাহায্য")
def help_msg(message):
    bot.reply_to(message, "সরাসরি আইপি অ্যাড্রেস লিখে পাঠান। উদাহরণ: `103.145.116.22`", parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_msg(message):
    if "." in message.text and len(message.text) > 6:
        save_user(message)
        process_ip(message, message.text.strip())

def process_ip(message, ip):
    bot.send_chat_action(message.chat.id, 'find_location')
    data = get_location_info(ip)
    
    if data and data['status'] == 'success':
        flag = "🇧🇩" if data['countryCode'] == "BD" else "🇮🇳" if data['countryCode'] == "IN" else "🌍"
        maps = f"https://www.google.com/maps?q={data['lat']},{data['lon']}"
        
        info = (
            f"┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
            f"     🚀 আইপি ট্র্যাকিং রেজাল্ট\n"
            f"┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
            f"🌐 **IP:** `{data['query']}`\n"
            f"{flag} **দেশ:** {data['country']}\n"
            f"🏙 **শহর:** {data['city']}\n"
            f"🏢 **ISP:** {data['isp']}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🔗 **[ম্যাপে লোকেশন দেখুন]({maps})**\n\n"
            f"🛡️ Developed by **{MY_NAME}**"
        )
        bot.send_message(message.chat.id, info, parse_mode="Markdown", disable_web_page_preview=False)
    else:
        bot.reply_to(message, "❌ দুঃখিত, আইপিটি ভুল অথবা কোনো তথ্য পাওয়া যায়নি।")

if __name__ == "__main__":
    show_banner()
    print(f"Jarvis is now active for BOSS {MY_NAME}!")
    bot.infinity_polling()

