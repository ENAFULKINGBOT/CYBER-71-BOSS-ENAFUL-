import telebot
from telebot import types

API_TOKEN = '8034344716:AAFeFDfTFCFd9Vl97FlrP5wMlLTrIhtxEw4'
bot = telebot.TeleBot(API_TOKEN, threaded=True)

MASTER_TEXT = (
    "━━━━━━━━━━━━━━━━━━━━\n"
    "🚀 **বট মালিক:** `এনাফুল`\n"
    "🤖 **অবস্থা:** `সক্রিয়` 🟢\n"
    "🛡️ **পাওয়ার্ড বাই:** `সাইবার ৭১` \n\n"
    "✨ **বটের ক্ষমতা:**\n"
    "🔹 মুহূর্তেই আপনার চ্যাট আইডি বের করা।\n"
    "🔹 যেকোনো ভিডিও বা ছবির ফাইল আইডি দেওয়া।\n"
    "🔹 আপনার প্রোফাইলের বিস্তারিত তথ্য দেখানো।\n\n"
    "🔗 **চ্যানেলে জয়েন করুন:** @KING_OF_ENAFUL\n"
    "━━━━━━━━━━━━━━━━━━━━"
)

photo_url = "https://w8chatid.netlify.app/avatar.jpg"

def get_main_markup():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="🆔 Get My ID", callback_data="get_id")
    btn2 = types.InlineKeyboardButton(text="📢 Join Channel", url="https://t.me/KING_OF_ENAFUL")
    markup.add(btn1, btn2)
    return markup

@bot.message_handler(commands=['start', 'help'])
def send_master_welcome(message):
    try:
        bot.send_photo(
            message.chat.id, 
            photo_url, 
            caption=f"👋 **Welcome, BOSS ENAFUL!**\n\n{MASTER_TEXT}\n\n🆔 আপনার আইডি: `{message.chat.id}`", 
            reply_markup=get_main_markup(), 
            parse_mode="Markdown"
        )
    except Exception as e:
        bot.send_message(
            message.chat.id, 
            f"{MASTER_TEXT}\n\n🆔 আপনার আইডি: `{message.chat.id}`", 
            reply_markup=get_main_markup(), 
            parse_mode="Markdown"
        )

@bot.callback_query_handler(func=lambda call: call.data == "get_id")
def callback_inline(call):
    id_response = (
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🆔 **আপনার চ্যাট আইডি:** `{call.message.chat.id}`\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"✨ আইডির ওপর টাচ করলে অটো কপি হবে।"
    )
    bot.answer_callback_query(call.id, "আইডি পাওয়া গেছে ✅")
    bot.send_message(call.message.chat.id, id_response, parse_mode="Markdown")

@bot.message_handler(content_types=['document', 'photo', 'video', 'sticker'])
def get_file_id(message):
    f_id = ""
    if message.content_type == 'document': f_id = message.document.file_id
    elif message.content_type == 'photo': f_id = message.photo[-1].file_id
    elif message.content_type == 'video': f_id = message.video.file_id
    else: f_id = message.sticker.file_id
    
    bot.reply_to(message, f"📂 **ফাইল আইডি:**\n\n`{f_id}`\n\n{MASTER_TEXT}", parse_mode="Markdown")

print("⚡ BOSS ENAFUL, Your 24/7 Master Bot is Ready!")
bot.infinity_polling(timeout=10, long_polling_timeout=5)

