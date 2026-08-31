import os

def fix_reply_kb():
    with open('keyboards/reply_kb.py', 'r', encoding='utf-8') as f:
        text = f.read()
    text = text.replace('style="success"', 'style="primary"')
    with open('keyboards/reply_kb.py', 'w', encoding='utf-8') as f:
        f.write(text)

def fix_inline_kb():
    with open('keyboards/inline_kb.py', 'r', encoding='utf-8') as f:
        text = f.read()
    
    # We want to change specific Mashhurlar / Yangi kinolar to primary
    # They are around lines 58, 62 in get_user_main_kb
    
    text = text.replace(
        'text=" Mashhurlar",\n                    callback_data="user:popular",\n                    style="success"',
        'text=" Mashhurlar",\n                    callback_data="user:popular",\n                    style="primary"'
    )
    text = text.replace(
        'text=" Yangi kinolar",\n                    callback_data="user:recent",\n                    style="success"',
        'text=" Yangi kinolar",\n                    callback_data="user:recent",\n                    style="primary"'
    )
    
    # Check get_search_movie_kb
    text = text.replace(
        'text=" Mashhurlar",\n                    callback_data="user:popular",\n                    style="success"',
        'text=" Mashhurlar",\n                    callback_data="user:popular",\n                    style="primary"'
    )
    
    # Check get_movie_detail_kb (it has 'success' for the movie button maybe?)
    # " Kino qidirish" is already primary.
    
    with open('keyboards/inline_kb.py', 'w', encoding='utf-8') as f:
        f.write(text)

fix_reply_kb()
fix_inline_kb()
print("Fixed colors")
