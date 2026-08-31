import os

def run():
    with open('handlers/admin.py', 'r', encoding='utf-8') as f:
        text = f.read()

    old_block = '''    if not message.forward_from_chat:
        text = (
            f"{PE_CROSS} <b>Noto'g'ri format</b>\\n\\n"
            f"{PE_INFO} Iltimos, kanaldagi xabarni forward qiling."
        )
        await message.answer(text, parse_mode="HTML")
        return

    chat = message.forward_from_chat
    channel_id = chat.id
    channel_username = chat.username
    channel_title = chat.title

    # Bot kanalda admin ekanligini tekshirish
    try:
        bot_member = await bot.get_chat_member(
            chat_id=channel_id, user_id=(await bot.get_me()).id
        )
        if bot_member.status not in ("administrator", "creator"):
            text = (
                f"{PE_CROSS} <b>Bot kanalda admin emas</b>\\n\\n"
                f"{PE_INFO} Avval botni kanalga admin qilib qo'shing."
            )
            await message.answer(text, parse_mode="HTML")
            return
    except Exception:
        text = (
            f"{PE_WARNING} <b>Kanalni tekshirib bo'lmadi</b>\\n\\n"
            f"{PE_INFO} Bot kanalda admin ekanligiga ishonch hosil qiling."
        )
        await message.answer(text, parse_mode="HTML")
        return

    invite_link = None
    if not channel_username:
        try:
            link_obj = await bot.create_chat_invite_link(
                chat_id=channel_id,
                name="Kino Bot Zayavka",
                creates_join_request=True
            )
            invite_link = link_obj.invite_link
        except Exception:
            text = (
                f"{PE_CROSS} <b>Maxfiy kanal uchun link yaratib bo'lmadi</b>\\n\\n"
                f"{PE_INFO} Botga 'Foydalanuvchilarni qo'shish' huquqini bering."
            )
            await message.answer(text, parse_mode="HTML")
            return'''

    new_block = '''    chat = None
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
    channel_title = chat.title or "Kanal"

    # Bot kanalda admin ekanligini tekshirish
    try:
        bot_member = await bot.get_chat_member(
            chat_id=channel_id, user_id=(await bot.get_me()).id
        )
        if bot_member.status not in ("administrator", "creator"):
            text = (
                f"{PE_CROSS} <b>Bot kanalda admin emas</b>\\n\\n"
                f"{PE_INFO} Avval botni <b>{channel_title}</b> kanaliga admin qilib qo'shing."
            )
            await message.answer(text, parse_mode="HTML")
            return
    except Exception as e:
        text = (
            f"{PE_WARNING} <b>Kanalni tekshirib bo'lmadi</b>\\n\\n"
            f"{PE_INFO} Bot kanalda admin emas yoki kanal topilmadi.\\n"
            f"<i>Xatolik: {e}</i>"
        )
        await message.answer(text, parse_mode="HTML")
        return

    invite_link = None
    if not channel_username:
        try:
            link_obj = await bot.create_chat_invite_link(
                chat_id=channel_id,
                name="Kino Bot Zayavka",
                creates_join_request=True
            )
            invite_link = link_obj.invite_link
        except Exception as e:
            text = (
                f"{PE_CROSS} <b>Maxfiy kanal uchun link yaratib bo'lmadi</b>\\n\\n"
                f"{PE_INFO} Botga 'Foydalanuvchilarni qo'shish' huquqini bering.\\n"
                f"<i>Xatolik: {e}</i>"
            )
            await message.answer(text, parse_mode="HTML")
            return'''

    if old_block in text:
        text = text.replace(old_block, new_block)
        with open('handlers/admin.py', 'w', encoding='utf-8') as f:
            f.write(text)
        print("Replaced successfully!")
    else:
        print("Block not found!")

run()
