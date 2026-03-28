import os, sys, time, random, datetime, re, multiprocessing, socket, json

import warnings
warnings.filterwarnings("ignore")

def modules():
    os.system('pkg update -y && pkg upgrade -y')
    os.system('clear')
    try: 
        import rich
    except ModuleNotFoundError:
        print("\x1b[1;92m RICH IS BEING INSTALLED... \033[1;37m")
        os.system('pip install rich --quiet')
    try:
        import bs4
    except ModuleNotFoundError:
        print("\x1b[1;92m BS4 IS BEING INSTALLED... \033[1;37m")
        os.system('pip install bs4 --quiet')
    try:
        import requests
    except ModuleNotFoundError:
        print("\x1b[1;92m REQUESTS IS BEING INSTALLED... \033[1;37m")
        os.system('pip install requests --quiet')

try:
    import requests
    from bs4 import BeautifulSoup as bs
    import urllib3, rich
    from rich.console import Console
    from concurrent.futures import ThreadPoolExecutor as ThreadPool
except ModuleNotFoundError:
    modules()
    import requests
    from bs4 import BeautifulSoup as bs

P = '\x1b[1;97m'
H = '\x1b[1;92m'
m = '\x1b[1;91m'
O = '\x1b[38;5;50m'

logo = (f'''\033[1;37m                                 
\x1b[38;5;45m██████╗  ██████╗ ███████╗███████╗
\033[97;1m██╔══██╗██╔═══██╗██╔════╝██╔════╝
\033[1;35m██████╔╝██║   ██║███████╗███████╗
\033[97;1m██╔══██╗██║   ██║╚════██║╚════██║
\033[0;96m██████╔╝╚██████╔╝███████║███████║
\x1b[38;5;208m╚═════╝  ╚═════╝ ╚══════╝╚══════╝
\x1b[38;5;46m███████╗███╗   ██╗ █████╗ ███████╗██╗   ██╗██╗     
\033[97;1m██╔════╝████╗  ██║██╔══██╗██╔════╝██║   ██║██║     
\033[1;35m█████╗  ██╔██╗ ██║███████║█████╗  ██║   ██║██║     
\033[97;1m██╔══╝  ██║╚██╗██║██╔══██║██╔══╝  ██║   ██║██║     
\033[0;96m███████╗██║ ╚████║██║  ██║██║     ╚██████╔╝███████╗
\x1b[38;5;208m╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚══════╝
 \033[1;34m=================================================
 \033[1;97m[\033[1;92m•\033[1;97m] Owner    : \x1b[38;5;45mBOSS ENAFUL
 \033[1;97m[\033[1;92m•\033[1;97m] Facebook : \033[1;35m丰ツቌ፝ ENAFUL ቌ፝ツ丰 
 \033[1;97m[\033[1;92m•\033[1;97m] Status   : \033[1;92m[PERSONAL]
 \033[1;97m[\033[1;92m•\033[1;97m]          \x1b[38;5;208mFACEBOOK DUMP TOOL🔥 
 \033[1;31m=================================================''')

def clear():
    os.system('clear')

def linex():
    print('\033[1;35m =================================================\x1b[1;97m')

def animation(u):
    for e in u + "\n":
        sys.stdout.write(e)
        sys.stdout.flush()
        time.sleep(0.01)


def entr():
    clear()
    print(logo)
    print(f" {H}[1]{P} LOGIN TOOL BY COOKIE")
    print(f" {H}[2]{P} WITHOUT COOKIE MENU")
    print(f" {H}[0]{P} CONTACT ADMIN")
    linex()
    choice = input(f' {H}Choice : {P}')
    if choice == '1':
        print("\n [!] Login system coming soon...")
    elif choice == '2':        
        print("\n [!] Without cookie system coming soon...")
    elif choice == '0':        
        os.system('xdg-open https://facebook.com/your_profile')
    else:
        linex()
        animation(' [!] SELECT CORRECTLY ')
        time.sleep(2)
        entr()

if __name__ == "__main__":
    entr()

