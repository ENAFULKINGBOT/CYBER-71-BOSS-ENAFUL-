import telebot
from telebot import types
from PIL import Image
from PIL.ExifTags import TAGS
import os
import time

R = '\033[1;31m'
G = '\033[1;32m'
Y = '\033[1;33m'
C = '\033[1;36m'
W = '\033[1;37m'
RE = '\033[0m'

def boss_banner():
    os.system('clear')
    print(f"{R} ██████╗  ██████╗ ███████╗███████╗{RE}")
    print(f"{R} ██╔══██╗██╔═══██╗██╔════╝██╔════╝{RE}")
    print(f"{Y} ██████╔╝██║   ██║███████╗███████╗{RE}")
    print(f"{Y} ██╔══██╗██║   ██║╚════██║╚════██║{RE}")
    print(f"{G} ██████╔╝╚██████╔╝███████║███████║{RE}")
    print(f"{G} ╚═════╝  ╚═════╝ ╚══════╝╚══════╝{RE}")
    print(f"{C}          OWNER: BOSS ENAFUL{RE}")
    print(f"{C}====================================={RE}")

 TOKEN = '8626038579:AAHBhTPxoqPjWc-WQ9Q1vAZQ47dqvxqID4o'
bot = telebot.TeleBot(TOKEN)
BOSS ENAFUL = "BOSS ENAFUL"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_msg = (f"🌟 **স্বাগতম বস!** 🌟\n\n"
                   f"আমি আপনার পার্সোনাল গ্যালারি ইনফো বট।\n"
                   f"যেকোনো ছবি পাঠান, আমি তার তথ্য বের করে দেব।\n\n"
                   f"🛡️ **Developed By:** {BOSS ENAFUL}")
    bot.send_message(message.chat.id, welcome_msg, parse_mode='Markdown')

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    sent_msg = bot.reply_to(message, "⚙️ এনালাইসিস করা হচ্ছে...")
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_name = "temp_image.jpg"
    
    with open(file_name, 'wb') as f:
        f.write(downloaded_file)

    try:
        img = Image.open(file_name)
        width, height = img.size
        f_size = os.path.getsize(file_name) / 1024 
        
        info_str = (f"📸 **PHOTO METADATA**\n"
                   f"━━━━━━━━━━━━━━━━━━━━\n"
                   f"👤 **Owner:** {BOSS ENAFUL}\n"
                   f"📏 **Resolution:** {width}x{height}\n"
                   f"📁 **Size:** {f_size:.2f} KB\n"
                   f"━━━━━━━━━━━━━━━━━━━━")
        bot.edit_message_text(info_str, message.chat.id, sent_msg.message_id, parse_mode='Markdown')
    except Exception as e:
        bot.edit_message_text(f"❌ এরর: {str(e)}", message.chat.id, sent_msg.message_id)
    finally:
        if os.path.exists(file_name):
            os.remove(file_name)

if __name__ == "__main__":
    boss_banner()
    print(f"{G}[+] বট সফলভাবে চালু হয়েছে...{RE}")
    bot.polling()
