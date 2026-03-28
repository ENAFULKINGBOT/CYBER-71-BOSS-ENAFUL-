import base64

filename = 'REAL_CODE.py'

def decrypt(file):
    try:
        with open(file, 'r') as f:
            data = f.read()
        
        if "b'" in data:
            code = data.split("b'")[-1].split("'")[0]
            decoded = base64.b64decode(code[::-1]).decode('utf-8')
            
            with open('FINAL_SOURCE.py', 'w') as f:
                f.write(decoded)
            return True
        else:
            return False
    except:
        return False

print("Breaking layers... Please wait.")
count = 0
while decrypt(filename):
    filename = 'FINAL_SOURCE.py'
    count += 1
    print(f"Layer {count} broken!")

print("\nAll layers are broken! Open 'FINAL_SOURCE.py' to see the real code.")

