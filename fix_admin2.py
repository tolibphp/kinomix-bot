import re

with open('handlers/admin.py', 'r', encoding='utf-8') as f:
    c = f.read()

c = re.sub(r'if message\.text and message\.text\.strip\(\) == .*Bekor qilish.*:', 'if message.text and "Bekor qilish" in message.text:', c)

with open('handlers/admin.py', 'w', encoding='utf-8') as f:
    f.write(c)
