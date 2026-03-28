#!/bin/bash

# স্ক্রিন পরিষ্কার করা
clear

# ব্যানার প্রদর্শন (আপনার স্ক্রিনশট অনুযায়ী স্টাইল)
echo -e "\e[1;32m"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "      ELITE CYBER TERMINAL - OWNER: ENAFUL   "
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "\e[0m"

# প্রয়োজনীয় প্যাকেজ আপডেট ও চেক করা
echo -e "\e[1;34m[*] Checking System Requirements...\e[0m"
pkg update -y && pkg upgrade -y
pkg install python -y
pip install python-telegram-bot flask requests cloudflared

# Cloudflare Tunnel ব্যাকগ্রাউন্ডে চালু করা
echo -e "\e[1;34m[*] Starting Cloudflare Tunnel...\e[0m"
# এটি আপনার পোর্ট 5000 কে ইন্টারনেটে কানেক্ট করবে
nohup cloudflared tunnel --url http://127.0.0.1:5000 > /dev/null 2>&1 &

sleep 5

# আপনার পাইথন বট ফাইলটি রান করা
echo -e "\e[1;32m[+] ENAFUL Bot is launching...\e[0m"
python bot.py

