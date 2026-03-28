import telebot
from github import Github
import base64

TOKEN = '8725651688:AAGHjkYOTJnAYGiTLbsWOH17_K4Y9bw4sXg'
GITHUB_TOKEN = 'YOUR_GITHUB_PAT_TOKEN'
REPO_NAME = '007TEAMBOSSENAFUL/CYBER_71_BOSS'

bot = telebot.TeleBot(TOKEN)
g = Github(GITHUB_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🔥 *WELCOME TO BOSS ENAFUL BOT* 🔥\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🤖 *আমি কী কী করতে পারি?*\n"
        "✅ যেকোনো APK বা ZIP ফাইল গিটহাবে আপলোড করতে পারি।\n"
        "✅ সরাসরি আপনার ওয়েবসাইটে ডাউনলোড বাটন অ্যাড করতে পারি।\n"
        "✅ আপনার ফাইলগুলো 'files' ফোল্ডারে সেভ করে রাখতে পারি।\n\n"
        "💡 *কীভাবে ব্যবহার করবেন?*\n"
        "আমাকে সরাসরি একটি APK বা ZIP ফাইল পাঠিয়ে দিন, বাকিটা আমি দেখে নেব!"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    if message.document.file_name.endswith(('.apk', '.zip')):
        file_name = message.document.file_name
        bot.reply_to(message, f"⚙️ *{file_name}* প্রসেস করা হচ্ছে... দয়া করে অপেক্ষা করুন।", parse_mode='Markdown')

        try:
            repo = g.get_repo(REPO_NAME)
           
            file_info = bot.get_file(message.document.file_id)
            file_data = bot.download_file(file_info.file_path)
            
            repo.create_file(f"files/{file_name}", f"Upload by Bot: {file_name}", file_data)

            contents = repo.get_contents("index.html")
            old_html = base64.b64decode(contents.content).decode('utf-8')

            download_url = f"https://raw.githubusercontent.com/{REPO_NAME}/main/files/{file_name}"
            
            new_btn = f'<a href="{download_url}" class="btn" onclick="return authInstall(\'{file_name}\')">📥 DOWNLOAD {file_name}</a>\n            '

            if "" in old_html:
                new_html = old_html.replace("", new_btn)
                repo.update_file(contents.path, f"Website Update: {file_name}", new_html, contents.sha)
                
                success_msg = (
                    "✅ *SUCCESS! SYSTEM UPDATED.*\n"
                    f"📁 ফাইল: {file_name}\n"
                    "🌐 ওয়েবসাইট এখন লাইভ আপডেট হয়েছে।"
                )
                bot.reply_to(message, success_msg, parse_mode='Markdown')
            else:
                bot.reply_to(message, "❌ এরর: index.html এ `` ট্যাগটি খুঁজে পাওয়া যায়নি।")

        except Exception as e:
            bot.reply_to(message, f"❌ এরর ঘটেছে: {str(e)}")
    else:
        bot.reply_to(message, "⚠️ শুধুমাত্র APK বা ZIP ফাইল এলাউড।")

print("BOSS ENAFUL Bot is Running...")
bot.polling()

