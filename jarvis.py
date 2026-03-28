import logging
import uuid
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, ConversationHandler, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

NEW_BOT_NAME, NEW_BOT_USERNAME = range(2)
SET_NAME_CHOICE, SET_NAME_NEW = range(2, 4)
SET_ABOUT_CHOICE, SET_ABOUT_NEW = range(4, 6)
TOKEN_CHOICE, REVOKE_CHOICE = range(6, 8)
DELETE_CHOICE, DELETE_CONFIRM = range(8, 10)

ADMIN_ID = "@KING_OF_ENAFUL"
ADMIN_URL = "https://t.me/KING_OF_ENAFUL"

def init_db():
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS bots 
                      (user_id INTEGER, name TEXT, username TEXT, token TEXT, about TEXT)''')
    conn.commit()
    conn.close()

init_db()

def save_bot(user_id, name, username, token):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bots (user_id, name, username, token, about) VALUES (?, ?, ?, ?, ?)", 
                   (user_id, name, username, token, "No about text set."))
    conn.commit()
    conn.close()

def get_user_bots(user_id):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, username, token, about FROM bots WHERE user_id = ?", (user_id,))
    return cursor.fetchall()

def update_db(query, params):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def bot_list_keyboard(bots, prefix):
    return InlineKeyboardMarkup([[InlineKeyboardButton(f"@{b[1]}", callback_data=f"{prefix}_{b[1]}")] for b in bots])

async def post_init(application):
    commands = [
        BotCommand("start", "বট শুরু করুন"),
        BotCommand("newbot", "নতুন বট তৈরি"),
        BotCommand("mybots", "বটের তালিকা"),
        BotCommand("setname", "নাম পরিবর্তন"),
        BotCommand("setabouttext", "About টেক্সট পরিবর্তন"),
        BotCommand("token", "টোকেন দেখুন"),
        BotCommand("revoke", "টোকেন রিসেট"),
        BotCommand("deletebot", "বট ডিলিট"),
        BotCommand("cancel", "বাতিল করুন")
    ]
    await application.bot.set_my_commands(commands)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        f"Contact [{ADMIN_ID}]({ADMIN_URL}) for help.\n\n"
        "I can help you create and manage Telegram bots.\n\n"
        "**Commands:**\n"
        "/newbot - create a new bot\n"
        "/mybots - list your bots\n"
        "/setname - change bot name\n"
        "/setabouttext - change bot about\n"
        "/token - get bot token\n"
        "/revoke - reset bot token\n"
        "/deletebot - delete a bot"
    )
    await update.effective_message.reply_text(text, parse_mode='Markdown', disable_web_page_preview=True)

async def newbot_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Alright, a new bot. How are we going to call it?")
    return NEW_BOT_NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['tmp_n'] = update.message.text
    await update.message.reply_text("Good. Now choose a username (must end in 'bot'):")
    return NEW_BOT_USERNAME

async def get_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uname = update.message.text.replace("@", "")
    if not uname.lower().endswith('bot'):
        await update.message.reply_text("❌ Error: Must end in 'bot'. Try again:")
        return NEW_BOT_USERNAME
    token = f"{update.effective_user.id}:{uuid.uuid4().hex[:30]}"
    save_bot(update.effective_user.id, context.user_data['tmp_n'], uname, token)
    await update.message.reply_text(f"Done! Bot: t.me/{uname}\nToken: `{token}`", parse_mode='Markdown')
    return ConversationHandler.END

async def setname_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bots = get_user_bots(update.effective_user.id)
    if not bots: return await update.message.reply_text("No bots found.")
    await update.message.reply_text("Choose a bot to change name:", reply_markup=bot_list_keyboard(bots, "sn"))
    return SET_NAME_CHOICE

async def setname_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['target'] = query.data.split('_')[1]
    await query.edit_message_text(f"Send new name for @{context.user_data['target']}:")
    return SET_NAME_NEW

async def setname_final(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update_db("UPDATE bots SET name = ? WHERE user_id = ? AND username = ?", (update.message.text, update.effective_user.id, context.user_data['target']))
    await update.message.reply_text("✅ Name updated successfully!")
    return ConversationHandler.END

async def setabout_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bots = get_user_bots(update.effective_user.id)
    if not bots: return await update.message.reply_text("No bots found.")
    await update.message.reply_text("Choose a bot to change about text:", reply_markup=bot_list_keyboard(bots, "sa"))
    return SET_ABOUT_CHOICE

async def setabout_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['target'] = query.data.split('_')[1]
    await query.edit_message_text(f"Send new about text for @{context.user_data['target']}:")
    return SET_ABOUT_NEW

async def setabout_final(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update_db("UPDATE bots SET about = ? WHERE user_id = ? AND username = ?", (update.message.text, update.effective_user.id, context.user_data['target']))
    await update.message.reply_text("✅ About text updated!")
    return ConversationHandler.END

async def token_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bots = get_user_bots(update.effective_user.id)
    if not bots: return await update.message.reply_text("No bots found.")
    await update.message.reply_text("Choose a bot to see token:", reply_markup=bot_list_keyboard(bots, "tk"))
    return TOKEN_CHOICE

async def token_show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uname = query.data.split('_')[1]
    bots = get_user_bots(update.effective_user.id)
    token = next(b[2] for b in bots if b[1] == uname)
    await query.edit_message_text(f"Token for @{uname}:\n`{token}`", parse_mode='Markdown')
    return ConversationHandler.END

async def revoke_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bots = get_user_bots(update.effective_user.id)
    if not bots: return await update.message.reply_text("No bots found.")
    await update.message.reply_text("Choose a bot to revoke token:", reply_markup=bot_list_keyboard(bots, "rv"))
    return REVOKE_CHOICE

async def revoke_final(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uname = query.data.split('_')[1]
    new_token = f"{update.effective_user.id}:{uuid.uuid4().hex[:30]}"
    update_db("UPDATE bots SET token = ? WHERE user_id = ? AND username = ?", (new_token, update.effective_user.id, uname))
    await query.edit_message_text(f"✅ Token revoked! New token for @{uname}:\n`{new_token}`", parse_mode='Markdown')
    return ConversationHandler.END

async def delete_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bots = get_user_bots(update.effective_user.id)
    if not bots: return await update.message.reply_text("No bots found.")
    await update.message.reply_text("Choose a bot to delete:", reply_markup=bot_list_keyboard(bots, "dl"))
    return DELETE_CHOICE

async def delete_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uname = query.data.split('_')[1]
    context.user_data['del_target'] = uname
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Yes, Delete It", callback_data="confirm_delete"), InlineKeyboardButton("No, Cancel", callback_data="cancel")]])
    await query.edit_message_text(f"⚠️ Are you sure you want to delete @{uname}?", reply_markup=keyboard)
    return DELETE_CONFIRM

async def delete_final(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "confirm_delete":
        update_db("DELETE FROM bots WHERE user_id = ? AND username = ?", (update.effective_user.id, context.user_data['del_target']))
        await query.edit_message_text(f"🗑 @{context.user_data['del_target']} deleted.")
    else:
        await query.edit_message_text("Cancelled.")
    return ConversationHandler.END

async def mybots(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bots = get_user_bots(update.effective_user.id)
    if not bots: return await update.message.reply_text("No bots found.")
    res = "📂 **Your Bots:**\n\n"
    for b in bots: res += f"• {b[0]} (@{b[1]})\nAbout: {b[3]}\nToken: `{b[2]}`\n\n"
    await update.message.reply_text(res, parse_mode='Markdown')

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("❌ Cancelled.")
    return ConversationHandler.END

if __name__ == '__main__':
    TOKEN = "8335716255:AAH1pLjgSK77a23RiTwDP7plnzP169Et7j4"
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()

    handlers = [
        ConversationHandler(entry_points=[CommandHandler('newbot', newbot_entry)], states={NEW_BOT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)], NEW_BOT_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_username)]}, fallbacks=[CommandHandler('cancel', cancel)]),
        ConversationHandler(entry_points=[CommandHandler('setname', setname_start)], states={SET_NAME_CHOICE: [CallbackQueryHandler(setname_choice, pattern="^sn_")], SET_NAME_NEW: [MessageHandler(filters.TEXT & ~filters.COMMAND, setname_final)]}, fallbacks=[CommandHandler('cancel', cancel)]),
        ConversationHandler(entry_points=[CommandHandler('setabouttext', setabout_start)], states={SET_ABOUT_CHOICE: [CallbackQueryHandler(setabout_choice, pattern="^sa_")], SET_ABOUT_NEW: [MessageHandler(filters.TEXT & ~filters.COMMAND, setabout_final)]}, fallbacks=[CommandHandler('cancel', cancel)]),
        ConversationHandler(entry_points=[CommandHandler('token', token_start)], states={TOKEN_CHOICE: [CallbackQueryHandler(token_show, pattern="^tk_")]}, fallbacks=[CommandHandler('cancel', cancel)]),
        ConversationHandler(entry_points=[CommandHandler('revoke', revoke_start)], states={REVOKE_CHOICE: [CallbackQueryHandler(revoke_final, pattern="^rv_")]}, fallbacks=[CommandHandler('cancel', cancel)]),
        ConversationHandler(entry_points=[CommandHandler('deletebot', delete_start)], states={DELETE_CHOICE: [CallbackQueryHandler(delete_confirm, pattern="^dl_")], DELETE_CONFIRM: [CallbackQueryHandler(delete_final, pattern="^(confirm_delete|cancel)$")]}, fallbacks=[CommandHandler('cancel', cancel)])
    ]

    for h in handlers: app.add_handler(h)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mybots", mybots))

    print("Jarvis is online with full BotFather features...")
    app.run_polling()

