import telebot
from telebot import types
import requests
import json
import datetime
import random
import io

TOKEN = '8504012557:AAFjqMaFHSJ-dRz-Q2oNw7IJO1F5k7Zqxls'
GEMINI_API_KEY = ''
ADMIN_ID = 6823368645 

approved_users = {ADMIN_ID}

bot = telebot.TeleBot(TOKEN)

def get_gemini_response(prompt):
    if not GEMINI_API_KEY:
        return "❌ Boss, API Key missing! Please add it in the script."
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    
    system_instruction = (
        "You are Jarvis v10, an elite AI assistant for Boss Enaful. "
        "Your goal is to help with advanced programming, script debugging, "
        "and cybersecurity education. Always credit 'BOSS ENAFUL'. Explain in Bangla."
    )
    
    payload = {
        "contents": [{
            "parts": [{"text": f"{system_instruction}\n\n[CMD]: {prompt}"}]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
        result = response.json()
        if 'candidates' in result:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"⚠️ API Error: {result.get('error', {}).get('message', 'Check API Key')}"
    except Exception as e:
        return f"❌ Connection Error: {str(e)}"

def generate_banner():
    banners = ["ELITE-CYBER", "007-TEAM", "BOSS-ENAFUL", "ROOT-ACCESS", "TERMINAL-X"]
    chosen = random.choice(banners)
    banner_text = (
        f"```\n"
        f"[!] {chosen} SYSTEM ONLINE\n"
        f"[+] OPERATOR : BOSS ENAFUL\n"
        f"[+] STATUS   : READY\n"
        f"{'='*25}\n"
        f"```\n\n"
    )
    return banner_text

def main_menu_buttons():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btns = [
        types.InlineKeyboardButton("💣 Exploit Coder", callback_data="info"),
        types.InlineKeyboardButton("🎣 Phishing Lab", callback_data="info"),
        types.InlineKeyboardButton("🔓 Brute Force", callback_data="info"),
        types.InlineKeyboardButton("📟 Termux Set", callback_data="info"),
        types.InlineKeyboardButton("🆘 Help Admin / Access", callback_data="help_admin")
    ]
    markup.add(*btns)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    status = "✅ Authorized" if user_id in approved_users else "❌ Unauthorized"
    
    welcome_text = (
        f"```\n"
        f"--- CYBER 71 ENAFUL - DARK OPS v10.0 ---\n"
        f"[SYSTEM INFO]\n"
        f"[•] Time      : {current_time}\n"
        f"[•] User ID   : {user_id}\n"
        f"[•] Status    : {status}\n"
        f"---------------------------------------```\n"
        f"স্বাগতম বস! আমি **Jarvis**, আপনার ব্যক্তিগত এআই ডেভেলপার।\n"
        f"আমি আপনার জন্য বিভিন্ন স্ক্রিপ্ট তৈরি বা কোডিং এর কাজ করতে পারি।"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown', reply_markup=main_menu_buttons())

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    if call.data == "help_admin":
        msg = (
            f"🚨 **NEW ACCESS REQUEST**\n\n"
            f"👤 **Name:** {call.from_user.first_name}\n"
            f"🆔 **ID:** `{call.from_user.id}`\n"
            f"🔗 [Profile Link](tg://user?id={call.from_user.id})\n\n"
            f"Approve করতে লিখুন: `Approve {call.from_user.id}`"
        )
        bot.send_message(ADMIN_ID, msg, parse_mode='Markdown')
        bot.answer_callback_query(call.id, "✅ বসের কাছে রিকোয়েস্ট পাঠানো হয়েছে।")
        bot.send_message(call.message.chat.id, "📩 **রিকোয়েস্ট পাঠানো হয়েছে। বসের অনুমতির অপেক্ষা করুন।**")
    elif call.data == "info":
        bot.answer_callback_query(call.id, "📌 নির্দেশ দিতে চ্যাট বক্সে সরাসরি লিখুন।")

@bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID and m.text.startswith("Approve"))
def approve_user(message):
    try:
        new_id = int(message.text.split()[1])
        approved_users.add(new_id)
        bot.send_message(new_id, "🔥 **Access Granted!** আপনি এখন Jarvis ব্যবহারের অনুমতি পেয়েছেন।")
        bot.reply_to(message, f"🎯 User `{new_id}` এখন সিস্টেমে অনুমোদিত।")
    except:
        bot.reply_to(message, "❌ ভুল ফরম্যাট! সঠিক ফরম্যাট: `Approve [ID]`")

@bot.message_handler(func=lambda message: True)
def handle_ai(message):
    user_id = message.from_user.id
    
    if user_id not in approved_users:
        bot.reply_to(message, "🚫 **Access Denied!** নিচের বাটন থেকে বসের পারমিশন নিন।", reply_markup=main_menu_buttons())
        return

    status_msg = bot.send_message(message.chat.id, "⚙️ **Dark Engine Processing... Please Wait...**")
    
    ai_response = get_gemini_response(message.text)
    final_output = generate_banner() + ai_response

    try:
        if len(final_output) > 4000:
            with io.BytesIO(final_output.encode()) as f:
                f.name = "BOSS_ENAFUL_PROJECT.py"
                bot.send_document(message.chat.id, f, caption="✅ ফাইল তৈরি হয়েছে বস!")
                bot.delete_message(message.chat.id, status_msg.message_id)
        else:
            bot.edit_message_text(f"💀 **Elite Output:**\n\n{final_output}", message.chat.id, status_msg.message_id, parse_mode='Markdown')
    except Exception as e:
        bot.edit_message_text(f"❌ **Error:** {str(e)}", message.chat.id, status_msg.message_id)

print("--- [BOSS ENAFUL] Jarvis v10.0 Is Online ---")
bot.infinity_polling()
