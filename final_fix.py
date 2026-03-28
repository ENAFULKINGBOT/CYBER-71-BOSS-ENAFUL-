import base64
import marshal
import zlib

data = "p1T0tGcx..."

try:
    decoded = base64.b64decode(data[::-1])
    
    source_code = marshal.loads(decoded)
    
    with open('FINAL_DONE.py', 'w') as f:
        f.write(str(source_code))
        
    print("\033[1;32m[+] Success! আসল কোড FINAL_DONE.py ফাইলে সেভ হয়েছে।")
except Exception as e:
    print(f"\033[1;31m[!] ভুল হয়েছে: {e}")

