import os

def run():
    with open('handlers/admin.py', 'r', encoding='utf-8') as f:
        text = f.read()

    old_block = '''    if not channel_username:
        text = (
            f"{PE_CROSS} <b>Kanal username'siz</b>\\n\\n"
            f"{PE_INFO} Faqat public (username'li) kanallar qo'shilishi mumkin."
        )
        await message.answer(text, parse_mode="HTML")
        return

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

    success = await db.add_channel(channel_id, channel_username, channel_title)
    await state.clear()

    if success:
        text = (
            f"{PE_CHECK} <b>Kanal qo'shildi!</b>\\n"
            f"{'━' * 28}\\n\\n"
            f"{PE_CHANNEL} {channel_title}\\n"
            f"{PE_GLOBE} @{channel_username}"
        )'''

    new_block = '''    # Bot kanalda admin ekanligini tekshirish
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
            return

    success = await db.add_channel(channel_id, channel_username, channel_title, invite_link)
    await state.clear()

    if success:
        text = (
            f"{PE_CHECK} <b>Kanal qo'shildi!</b>\\n"
            f"{'━' * 28}\\n\\n"
            f"{PE_CHANNEL} {channel_title}\\n"
        )
        if channel_username:
            text += f"{PE_GLOBE} @{channel_username}"
        else:
            text += f"{PE_LOCK} Maxfiy kanal (Zayavka orqali)"'''

    if old_block in text:
        text = text.replace(old_block, new_block)
        with open('handlers/admin.py', 'w', encoding='utf-8') as f:
            f.write(text)
        print("Replaced!")
    else:
        print("Block not found!")

run()
