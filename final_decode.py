import base64
import marshal

data = 'আপনার_লম্বা_কোড_এখানে_পেস্ট_করুন'

try:
    decoded = base64.b64decode(data)
    source = marshal.loads(decoded)
    print("\n[+] Success! কোড পাওয়া গেছে:\n")
    print(source)
except:
    try:
        decoded = base64.b64decode(data[::-1])
        source = marshal.loads(decoded)
        print("\n[+] Success (Reversed)! কোড পাওয়া গেছে:\n")
        print(source)
    except Exception as e:
        print(f"\n[!] এরর: {e}")
        print("সম্ভবত ডাটা কপি করতে ভুল হয়েছে।")

