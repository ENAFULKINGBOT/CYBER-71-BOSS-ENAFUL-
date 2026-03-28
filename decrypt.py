import base64

with open('KAMRUL-2026.py', 'r') as f:
    content = f.read()

try:
    data = content.split("b'")[-1].split("'")[0]
    decoded_code = base64.b64decode(data[::-1]).decode('utf-8')
    
    with open('MAIN_CODE.py', 'w') as f:
        f.write(decoded_code)
    print("Success! Your main code is saved in MAIN_CODE.py")
except Exception as e:
    print("Error:", e)

