import sys

target_file = 'KAMRUL-2026.py'

def mock_exec(object, globals=None, locals=None):
    print("\n--- [ REAL CODE FOUND ] ---\n")
    if isinstance(object, str):
        print(object)
    else:
        import marshal
        try:
            print(marshal.loads(object))
        except:
            print("Successfully Captured Code!")
    print("\n--- [ END OF CODE ] ---\n")
    sys.exit()

__builtins__.exec = mock_exec

try:
    with open(target_file, 'r') as f:
        exec(f.read())
except Exception as e:
    print(f"Error: {e}")

