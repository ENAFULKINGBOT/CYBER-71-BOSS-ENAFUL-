import telebot
from telebot import types
from flask import Flask, request, render_template_string, redirect, session, url_for, send_from_directory
import os
from threading import Thread
import datetime

API_TOKEN = '8756220877:AAGKKlYU8MDptXx2b5-EvCG_hwgRREhDfQk' 
ADMIN_USERNAME = 'CYBER_71_ENAFUL' 
UPLOAD_FOLDER = 'uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)
app.secret_key = "jarvis_full_matrix_v7"

def track_visitor(req, status="ATTEMPT"):
    ip = req.remote_addr
    ua = req.headers.get('User-Agent')
    timestamp = datetime.datetime.now().strftime("%I:%M:%S %p | %d-%m-%Y")
    msg = f"🛰 **JARVIS MATRIX LOG**\n━━━━━━━━━━━━\n👤 Status: `{status}`\n🕒 Time: `{timestamp}`\n🌐 IP: `{ip}`"
    try: bot.send_message(ADMIN_USERNAME, msg, parse_mode="Markdown")
    except: pass

MATRIX_BASE = """
<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
<style>
    body { background: #000; color: #0f0; font-family: 'Courier New', monospace; margin: 0; text-align: center; overflow: hidden; height: 100vh; }
    canvas { position: fixed; top: 0; left: 0; z-index: -1; opacity: 0.5; }
    .main-box { position: relative; z-index: 1; border: 2px solid #0f0; padding: 30px; border-radius: 10px; background: rgba(0, 10, 0, 0.9); box-shadow: 0 0 30px #0f0; display: inline-block; margin-top: 10vh; max-width: 90%; }
    h1 { color: red; text-shadow: 0 0 10px red; }
    .btn { background: transparent; border: 1px solid cyan; color: cyan; padding: 12px 25px; cursor: pointer; border-radius: 5px; margin-top: 15px; font-weight: bold; }
    a { color: lime; text-decoration: none; }
</style>
<canvas id="matrix_rain"></canvas>
<script>
    const canvas = document.getElementById('matrix_rain');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth; canvas.height = window.innerHeight;
    const chars = "01ENAFULJARVISMISHKAT💀☠💻";
    const drops = Array(Math.floor(canvas.width/16)).fill(1);
    function draw() {
        ctx.fillStyle = "rgba(0, 0, 0, 0.05)"; ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#0f0"; ctx.font = "16px monospace";
        drops.forEach((y, i) => {
            const text = chars[Math.floor(Math.random() * chars.length)];
            ctx.fillText(text, i * 16, y * 16);
            if (y * 16 > canvas.height && Math.random() > 0.975) drops[i] = 0;
            drops[i]++;
        });
    }
    setInterval(draw, 35);
</script>
"""

LOGIN_HTML = MATRIX_BASE + """
<div class="main-box">
    <h2 style="color:red;">[!] SYSTEM COMPROMISED [!]</h2>
    <h1>JARVIS AI ASSISTANT</h1>
    <p>Owner: Boss ENAFUL</p>
    <div style="border:1px solid #0f0; padding:10px; font-size:12px; margin:10px 0;">
        [+] SECURITY BYPASSED [+]<br>
        [+] DATABASE ACCESSED [+]
    </div>
    <button class="btn" onclick="startAI()">🎤 INITIALIZE ACCESS</button>
    <div id="status" style="margin-top:15px; color:yellow;">System Locked</div>
</div>
<script>
    function startAI() {
        let welcome = new SpeechSynthesisUtterance("Welcome My Boss ENAFUL. State your voice code.");
        window.speechSynthesis.speak(welcome);
        
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en-US';
        recognition.onresult = function(event) {
            const code = event.results[0][0].transcript.toLowerCase();
            if (code.includes("hello enaful boss")) {
                let ok = new SpeechSynthesisUtterance("Access granted. Opening vault.");
                window.speechSynthesis.speak(ok);
                window.location.href = "/auth_process";
            } else {
                document.getElementById('status').innerText = "Wrong Code! Access Denied.";
            }
        };
        recognition.start();
    }
</script>
"""

VAULT_HTML = MATRIX_BASE + """
<div class="main-box">
    <h1 style="color:cyan; text-shadow: 0 0 10px cyan;">🛡️ SECURE VAULT 🛡️</h1>
    <p style="color:white;">Welcome back, Boss Enaful.</p>
    <hr style="border:0.5px solid #0f0;">
    <div style="text-align:left; max-height: 300px; overflow-y: auto;">
        {{ files_list | safe }}
    </div>
    <br>
    <a href="/" style="color:red; font-size:12px;">[ LOGOUT SYSTEM ]</a>
</div>
"""

@app.route('/')
def index():
    return render_template_string(LOGIN_HTML)

@app.route('/auth_process')
def auth_process():
    session['logged_in'] = True
    track_visitor(request, "VOICE SUCCESS")
    return redirect(url_for('vault'))

@app.route('/vault')
def vault():
    if not session.get('logged_in'): return redirect(url_for('index'))
    files = os.listdir(UPLOAD_FOLDER)
    files_html = ""
    if not files:
        files_html = "<p style='color:yellow;'>ভল্টে বর্তমানে কোনো ফাইল নেই।</p>"
    else:
        for f in files:
            files_html += f"<p>📁 {f} | <a href='/download/{f}'>[DOWNLOAD]</a></p>"
    return render_template_string(VAULT_HTML, files_list=files_html)

@app.route('/download/<n>')
def download(n):
    if not session.get('logged_in'): return "Denied", 403
    return send_from_directory(UPLOAD_FOLDER, n)

if __name__ == '__main__':
    Thread(target=lambda: bot.infinity_polling()).start()
    app.run(host='0.0.0.0', port=5000)

