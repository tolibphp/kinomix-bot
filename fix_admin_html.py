import os
import html

def run():
    with open('handlers/admin.py', 'r', encoding='utf-8') as f:
        text = f.read()

    old_block = '''    success = await db.add_channel(channel_id, channel_username, channel_title, invite_link)
    await state.clear()

    if success:
        text = (
            f"{PE_CHECK} <b>Kanal qo'shildi!</b>\\n"
            f"{'➖' * 28}\\n\\n"
            f"{PE_CHANNEL} {channel_title}\\n"
        )
        if channel_username:
            text += f"{PE_GLOBE} @{channel_username}"
        else:
            text += f"{PE_LOCK} Maxfiy kanal (Zayavka orqali)"
    else:
        text = f"{PE_CROSS} <b>Kanal qo'shishda xatolik yuz berdi</b>"'''

    new_block = '''    import html
    safe_title = html.escape(channel_title) if channel_title else "Kanal"
    success = await db.add_channel(channel_id, channel_username, channel_title, invite_link)
    await state.clear()

    if success:
        text = (
            f"{PE_CHECK} <b>Kanal qo'shildi!</b>\\n"
            f"{'➖' * 28}\\n\\n"
            f"{PE_CHANNEL} <b>{safe_title}</b>\\n"
        )
        if channel_username:
            text += f"{PE_GLOBE} @{channel_username}"
        else:
            text += f"{PE_LOCK} Maxfiy kanal (Zayavka orqali)"
    else:
        text = f"{PE_CROSS} <b>Kanal qo'shishda xatolik yuz berdi</b>"'''

    if old_block in text:
        text = text.replace(old_block, new_block)
        with open('handlers/admin.py', 'w', encoding='utf-8') as f:
            f.write(text)
        print("Fixed HTML parse error in process_add_channel")
    else:
        print("Block not found in admin.py")

run()
