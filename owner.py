import telebot
from telebot import types
from flask import Flask, request, render_template_string, redirect, session, url_for, send_from_directory
import os

API_TOKEN = '8756220877:AAGKKlYU8MDptXx2b5-EvCG_hwgRREhDfQk' 
ADMIN_USERNAME = 'CYBER_71_ENAFUL' 
SERVER_URL = "https://standards-benchmark-norman-mentor.trycloudflare.com" 

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)
app.secret_key = "king_enaful_secret_v10"

HACK_THEME_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SYSTEM COMPROMISED - KING OF ENAFUL</title>
    <style>
        body { background-color: black; color: #00FF00; font-family: 'Courier New', monospace; margin: 0; text-align: center; overflow: hidden; }
        canvas { position: absolute; top: 0; left: 0; z-index: -1; }
        .main-container { position: relative; z-index: 1; padding-top: 50px; }
        h1 { color: red; text-shadow: 0 0 20px red; }
        .terminal-box { border: 1px solid #0f0; padding: 15px; background: rgba(0, 20, 0, 0.8); display: inline-block; width: 85%; max-width: 400px; text-align: left; font-size: 13px; margin-bottom: 20px;}
        .btn-group { display: flex; flex-direction: column; gap: 10px; align-items: center; }
        .btn { background: #0f0; color: #000; border: none; padding: 12px 30px; font-weight: bold; cursor: pointer; text-transform: uppercase; border-radius: 5px; width: 220px; text-decoration: none;}
        .btn-file { background: #f0f; box-shadow: 0 0 15px #f0f; }
    </style>
</head>
<body>
    <canvas id="matrix"></canvas>
    <div class="main-container">
        <h1>HACKED BY KING OF ENAFUL</h1>
        <div class="terminal-box">
            <div>[+] Initializing Bypass... Done.</div>
            <div>[+] System Compromised [+]</div>
            <div>[+] Admin: @CYBER_71_ENAFUL [+]</div>
            <div>[+] Welcome, KING OF ENAFUL.</div>
        </div>
        <div class="btn-group">
            <form action="/verify" method="POST"><button type="submit" class="btn">SCAN BIOMETRIC & ENTER</button></form>
            <a href="/files" class="btn btn-file">📁 VIEW SECURE FILES</a>
        </div>
    </div>
    <script>
        const canvas = document.getElementById('matrix');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        const letters = "010101010101ABCDEFHIJKLMNOPQRSTUVWXYZ";
        const fontSize = 16; const columns = canvas.width / fontSize;
        const drops = []; for (let i = 0; i < columns; i++) drops[i] = 1;
        function draw() {
            ctx.fillStyle = "rgba(0, 0, 0, 0.05)"; ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "#0F0"; ctx.font = fontSize + "px arial";
            for (let i = 0; i < drops.length; i++) {
                const text = letters.charAt(Math.floor(Math.random() * letters.length));
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            }
        }
        setInterval(draw, 33);
    </script>
</body>
</html>
"""

@app.route('/files')
def list_files():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    
    files = os.listdir(UPLOAD_FOLDER)
    file_list_html = """
    <style>
        body { background: #000; color: #0f0; font-family: monospace; padding: 20px; text-align: center; }
        .file-card { border: 1px solid #0f0; padding: 10px; margin: 10px auto; width: 80%; max-width: 500px; text-align: left; }
        a { color: #f0f; text-decoration: none; }
    </style>
    <h2>☣️ SECURE FILE VAULT - KING OF ENAFUL ☣️</h2>
    """
    for f in files:
        file_list_html += f'<div class="file-card">🔒 <a href="/download/{f}">{f}</a></div>'
    
    file_list_html += "<br><a href='/' style='color:white;'>[ EXIT ]</a>"
    return render_template_string(file_list_html)

@app.route('/download/<filename>')
def download_file(filename):
    if not session.get('logged_in'):
        return "❌ ACCESS DENIED!", 403
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/')
def index():
    return render_template_string(HACK_THEME_HTML)

@app.route('/verify', methods=['POST'])
def verify():
    session['logged_in'] = True
    bot.send_message(ADMIN_USERNAME, "🔓 **NOTICE:** Admin Panel has been accessed.")
    return redirect(url_for('list_files'))

@bot.message_handler(content_types=['document', 'photo', 'video'])
def handle_docs(message):
    if message.from_user.username == ADMIN_USERNAME:
        try:
            file_info = None
            if message.document:
                file_info = bot.get_file(message.document.file_id)
                file_name = message.document.file_name
            elif message.photo:
                file_info = bot.get_file(message.photo[-1].file_id)
                file_name = f"photo_{message.photo[-1].file_id}.jpg"
            
            downloaded_file = bot.download_file(file_info.file_path)
            with open(os.path.join(UPLOAD_FOLDER, file_name), 'wb') as new_file:
                new_file.write(downloaded_file)
            
            bot.reply_to(message, f"✅ **KING OF ENAFUL**, ফাইলটি আপনার সুরক্ষিত সার্ভারে রাখা হয়েছে।")
        except Exception as e:
            bot.reply_to(message, f"❌ ত্রুটি: {e}")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔗 Open Admin Panel", url=SERVER_URL))
    bot.reply_to(message, "👑 **Welcome KING OF ENAFUL!**\n\nবিনা অনুমতিতে কেউ আপনার ফাইল দেখতে পারবে না।", reply_markup=markup)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

