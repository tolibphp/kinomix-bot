import os

def fix_kb():
    with open('keyboards/inline_kb.py', 'r', encoding='utf-8') as f:
        text = f.read()
    
    text = text.replace('callback_data="popular_movies",\n            icon_custom_emoji_id=ID_FIRE,\n            style="success"', 'callback_data="popular_movies",\n            icon_custom_emoji_id=ID_FIRE,\n            style="primary"')
    text = text.replace('callback_data="recent_movies",\n            icon_custom_emoji_id=ID_SPARKLE,\n            style="success"', 'callback_data="recent_movies",\n            icon_custom_emoji_id=ID_SPARKLE,\n            style="primary"')
    text = text.replace('icon_custom_emoji_id=ID_CLAPPER,\n                style="success"', 'icon_custom_emoji_id=ID_CLAPPER,\n                style="primary"')
    
    with open('keyboards/inline_kb.py', 'w', encoding='utf-8') as f:
        f.write(text)

fix_kb()
print("Fixed remaining success styles.")
