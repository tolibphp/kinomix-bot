import re

def run():
    with open('handlers/admin.py', 'r', encoding='utf-8') as f:
        text = f.read()

    text = re.sub(
        r'success = await db\.add_channel\((.*?)\)\s*await state\.clear\(\)\s*if success:',
        r'success = await db.add_channel(\1)\n    await state.clear()\n\n    import html\n    safe_title = html.escape(channel_title) if channel_title else "Kanal"\n    if success:',
        text
    )

    with open('handlers/admin.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Done safe title!")

run()
