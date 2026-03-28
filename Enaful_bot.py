import telebot
from telebot import types
from google_play_scraper import search, app
import pyaxmlparser
import os

API_TOKEN = '8088612402:AAHUamGhc2H6jD2_Kj1IOaAnI1JqXf4c_X0'
YOUR_USERNAME = "KING_OF_ENAFUL" 

bot = telebot.TeleBot(API_TOKEN)

def get_markup(app_url):
    markup = types.InlineKeyboardMarkup(row_width=1)
    download_btn = types.InlineKeyboardButton(text="📥 Download App", url=app_url)
    owner_btn = types.InlineKeyboardButton(text="👤 Contact Owner (Enaful)", url=f"https://t.me/{YOUR_USERNAME}")
    markup.add(download_btn, owner_btn)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "✨ **Welcome to App Pro Assistant** ✨\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"👑 **BOT OWNER:** ENAFUL\n"
        f"🆔 **USER ID:** @{YOUR_USERNAME}\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "✅ অ্যাপের নাম লিখলে সাথে সাথে সব তথ্য পাবেন।\n"
        "✅ সরাসরি APK ফাইল পাঠিয়ে টোকেন চেক করতে পারবেন।\n"
        "━━━━━━━━━━━━━━━━━━━━"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def get_app_details(message):
    query = message.text.strip()
    status_msg = bot.reply_to(message, f"🚀 '{query}' এর তথ্য সংগ্রহ করছি...")
    
    try:
        search_results = search(query, n_hits=1)
        
        if not search_results:
            bot.edit_message_text(f"❌ '{query}' নামে কোনো অ্যাপ পাওয়া যায়নি।", message.chat.id, status_msg.message_id)
            return

        package_id = search_results[0]['appId']
        
        try:
            info = app(package_id, lang='en', country='us')
            app_name = info.get('title', 'N/A')
            description = info.get('summary') if info.get('summary') else "No description available."
            app_url = info.get('url', f"https://play.google.com/store/apps/details?id={package_id}")
            installs = info.get('installs', 'N/A')
            score = info.get('score', 'N/A')
        except:
            app_name = search_results[0]['title']
            description = "Click the button below to see full details."
            app_url = f"https://play.google.com/store/apps/details?id={package_id}"
            installs = "N/A"
            score = "N/A"

        response = (
            f"📱 **App Name:** {app_name}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🛠 **কাজ:** {description}\n\n"
            f"🔑 **টোকেন (ID):** `{package_id}`\n"
            f"📥 **ডাউনলোড:** {installs}\n"
            f"⭐ **রেটিং:** {score}\n\n"
            f"👤 **BOT OWNER:** ENAFUL\n"
            f"━━━━━━━━━━━━━━━━━━━━"
        )
        
        bot.edit_message_text(response, message.chat.id, status_msg.message_id, 
                             parse_mode="Markdown", reply_markup=get_markup(app_url))
                             
    except Exception as e:
        bot.edit_message_text(f"⚠️ দুঃখিত, তথ্য পাওয়া যায়নি! সঠিক নাম লিখুন।", message.chat.id, status_msg.message_id)

@bot.message_handler(content_types=['document'])
def handle_apk(message):
    if message.document.file_name.lower().endswith('.apk'):
        status_msg = bot.reply_to(message, "⏳ APK ফাইলটি চেক করছি...")
        file_path = ""
        try:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            file_path = message.document.file_name
            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)

            apk = pyaxmlparser.APK(file_path)
            package_id = apk.package
            app_name = apk.application
            play_store_link = f"https://play.google.com/store/apps/details?id={package_id}"

            response = (
                f"✅ **APK Details Found!**\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"📦 **App Name:** {app_name}\n"
                f"🔑 **অ্যাপ টোকেন (ID):** `{package_id}`\n\n"
                f"👤 **BOT OWNER:** ENAFUL\n"
                f"━━━━━━━━━━━━━━━━━━━━"
            )
            bot.edit_message_text(response, message.chat.id, status_msg.message_id, 
                                 parse_mode="Markdown", reply_markup=get_markup(play_store_link))
        except:
            bot.edit_message_text("⚠️ ফাইলটি প্রসেস করা সম্ভব হয়নি।", message.chat.id, status_msg.message_id)
        finally:
            if file_path and os.path.exists(file_path): os.remove(file_path)

if __name__ == "__main__":
    print(f"Jarvis আপনার বটটি এখন ১০০% সচল আছে...")
    bot.infinity_polling()

