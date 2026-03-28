import base64

with open('MAIN_CODE.py', 'r') as f:
    content = f.read()

try:
    data = content.split("b'")[-1].split("'")[0]
    final_code = base64.b64decode(data[::-1]).decode('utf-8')
    
    with open('REAL_CODE.py', 'w') as f:
        f.write(final_code)
    print("Success! Now check REAL_CODE.py")
except Exception as e:
    print("Failed to decrypt layer 2:", e)

