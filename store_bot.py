import telebot
from telebot import types

TOKEN = '8636773170:AAHA29qctVm_ksCRyKYnB7haP0yD_bBeUP8'
bot = telebot.TeleBot(TOKEN)

CHANNEL_URL = 'https://t.me/+xi6S4zVPjiplM2I1'

def get_main_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📹 YouTube Premium (Mod)", url="https://t.me/c/3649388708/41"),
        types.InlineKeyboardButton("🎮 Free Fire VIP Panel", url="https://t.me/c/3649388708/42"),
        types.InlineKeyboardButton("🛠️ DMSS 1.99.623 (File)", url="https://t.me/c/3649388708/43"),
        types.InlineKeyboardButton("🛡️ Kaspersky Antivirus", url="https://t.me/c/3649388708/44"),
        types.InlineKeyboardButton("💡 Other Mod Apps", url="https://t.me/c/3649388708/45"),
        types.InlineKeyboardButton("📢 Join Main Channel", url=CHANNEL_URL),
        types.InlineKeyboardButton("🛠️ Contact Admin", url="https://t.me/your_username_here")
    )
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "স্বাগতম! নিচে থেকে আপনার ফাইল বেছে নিন:", reply_markup=get_main_keyboard())

print("বটটি এখন লাইভ আছে...")
bot.polling()

