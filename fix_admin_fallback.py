import os

def run():
    with open('handlers/admin.py', 'r', encoding='utf-8') as f:
        text = f.read()

    old_block = '''    chat = None
    if message.forward_origin:
        if message.forward_origin.type == "channel":
            chat = message.forward_origin.chat
        elif message.forward_origin.type == "chat":
            chat = message.forward_origin.sender_chat
    
    if not chat and message.forward_from_chat:
        chat = message.forward_from_chat

    if not chat:
        text = (
            f"{PE_CROSS} <b>Noto'g'ri format</b>\\n\\n"
            f"{PE_INFO} Iltimos, kanaldagi xabarni forward qiling.\\n"
            f"<i>Balki kanal forward qilishni man etgan bo'lishi mumkin.</i>"
        )
        await message.answer(text, parse_mode="HTML")
        return

    channel_id = chat.id
    channel_username = chat.username
    channel_title = chat.title or "Kanal"'''

    new_block = '''    chat = None
    if message.forward_origin:
        if message.forward_origin.type == "channel":
            chat = message.forward_origin.chat
        elif message.forward_origin.type == "chat":
            chat = message.forward_origin.sender_chat
    
    if not chat and message.forward_from_chat:
        chat = message.forward_from_chat

    channel_id = None
    channel_username = None
    channel_title = "Kanal"

    if chat:
        channel_id = chat.id
        channel_username = chat.username
        channel_title = chat.title or "Kanal"
    elif message.text and (message.text.startswith("-100") or message.text.startswith("@")):
        try:
            # Fallback: manually typed ID or username
            chat = await bot.get_chat(message.text.strip())
            channel_id = chat.id
            channel_username = chat.username
            channel_title = chat.title or "Kanal"
        except Exception:
            text = (
                f"{PE_CROSS} <b>Kanal topilmadi</b>\\n\\n"
                f"{PE_INFO} Bot kanalda admin emas yoki ID/Username xato."
            )
            await message.answer(text, parse_mode="HTML")
            return
    else:
        text = (
            f"{PE_CROSS} <b>Noto'g'ri format</b>\\n\\n"
            f"{PE_INFO} Iltimos, kanaldagi xabarni forward qiling yoki kanal ID sini (-100...) yuboring.\\n"
            f"<i>Maxfiy kanallar ID sini bilish uchun xabarni @userinfobot ga forward qiling.</i>"
        )
        await message.answer(text, parse_mode="HTML")
        return'''

    if old_block in text:
        text = text.replace(old_block, new_block)
        with open('handlers/admin.py', 'w', encoding='utf-8') as f:
            f.write(text)
        print("Fallback added!")
    else:
        print("Block not found!")

run()
