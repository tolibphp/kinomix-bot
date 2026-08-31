import re

with open('handlers/admin.py', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('message.text.strip() == "\u2717 Bekor qilish"', '"Bekor qilish" in message.text')
c = c.replace('message.text.strip() == "❌ Bekor qilish"', '"Bekor qilish" in message.text')

with open('handlers/admin.py', 'w', encoding='utf-8') as f:
    f.write(c)
