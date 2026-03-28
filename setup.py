import os

os.system('clear')

def setup():
    banner = r"""
    echo -e "\e[1;36m┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓"
    echo -e "\e[1;31m         HACKED BY 007 TEAM         "
    echo -e "\e[1;36m┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
    echo -e "\e[1;32m[+] Operator : 007 TEAM"
    echo -e "\e[1;32m[+] Status   : READY\e[0m"
    """
    
    home = os.path.expanduser("~")
    with open(f"{home}/.bashrc", "a") as f:
        f.write(f"\n{banner}\n")
    
    print("\033[1;32m✅ Setup Success! Please Restart Termux.\033[0m")

if __name__ == "__main__":
    setup()

