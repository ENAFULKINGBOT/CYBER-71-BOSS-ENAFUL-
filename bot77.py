import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

TOKEN = '8676024624:AAH4OoRcAweKjXHl91lXVD-UGolgALP0OW4'
OWNER_USERNAME = '@KING_OF_ENAFUL'
BASE_URL = 'https://03a04ce5807be9.lhr.life'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = (
        f"┏━━━━━━━━━━━━━━━━━━━━━━┓\n"
        f"┃   🛡️ **CYBER-71 TERMINAL V4.0** 🛡️   ┃\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
        f"👤 **Operator:** `{user.first_name}`\n"
        f"📡 **Status:** `Active 🟢` \n"
        f"───────────────────────\n"
        f"নিচের বাটনে ক্লিক করুন, লিঙ্কটি মেসেজে আসবে।\n"
        f"───────────────────────"
    )

    keyboard = [
        [InlineKeyboardButton("🏰 ⟪ TOWER KING: AUTH ⟫", callback_data='get_link')],
        [InlineKeyboardButton("📍 TRACKING", callback_data='get_link')],
        [InlineKeyboardButton("📂 STORAGE", callback_data='get_link')],
        [InlineKeyboardButton("⚡ CONTACT", url=f"https://t.me/KING_OF_ENAFUL")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    msg = f"🔗 **Generated Link:**\n`{BASE_URL}`"
    await query.message.reply_text(msg, parse_mode='Markdown')

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.run_polling()

