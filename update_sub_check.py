import os

def run():
    with open('handlers/user.py', 'r', encoding='utf-8') as f:
        text = f.read()

    old_block = '''@router.callback_query(F.data == "check_subscription")
async def cb_check_subscription(
    callback: CallbackQuery, db: Database, bot: Bot
) -> None:
    user = callback.from_user
    channels = await db.get_channels()

    not_subscribed: list[dict] = []
    for ch in channels:
        try:
            member = await bot.get_chat_member(
                chat_id=ch["channel_id"], user_id=user.id
            )
            if member.status in ("left", "kicked"):
                not_subscribed.append(
                    {
                        "channel_id": ch["channel_id"],
                        "channel_username": ch["channel_username"],
                        "channel_title": ch["channel_title"],
                    }
                )
        except Exception:
            pass

    if not_subscribed:
        await callback.answer(
            "Hali barcha kanallarga obuna bo'lmagansiz!", show_alert=True
        )
        return

    await callback.answer("Tekshirish muvaffaqiyatli!", show_alert=True)'''

    new_block = '''@router.callback_query(F.data == "check_subscription")
async def cb_check_subscription(
    callback: CallbackQuery, db: Database, bot: Bot, state: FSMContext
) -> None:
    user = callback.from_user
    channels = await db.get_channels()

    not_subscribed: list[dict] = []
    for row in channels:
        ch = dict(row) if hasattr(row, "keys") else row
        try:
            member = await bot.get_chat_member(
                chat_id=ch["channel_id"], user_id=user.id
            )
            if member.status in ("left", "kicked"):
                has_req = await db.has_join_request(user.id, ch["channel_id"])
                if not has_req:
                    not_subscribed.append(ch)
        except Exception:
            has_req = await db.has_join_request(user.id, ch["channel_id"])
            if not has_req:
                not_subscribed.append(ch)

    if not_subscribed:
        await callback.answer(
            "Hali barcha kanallarga obuna bo'lmagansiz yoki zayavka tashlamagansiz!", show_alert=True
        )
        return

    await callback.answer("Tekshirish muvaffaqiyatli!", show_alert=False)
    
    # Delete the subscription message
    try:
        await callback.message.delete()
    except Exception:
        pass
        
    # Welcome the user
    text = (
        f"✅ <b>Barcha kanallarga a'zo bo'ldingiz (yoki zayavka qabul qilindi)!</b>\\n\\n"
        f"Endi botdan bemalol foydalanishingiz mumkin.\\n"
        f"Kino kodini yuboring yoki quyidagi tugmalardan foydalaning."
    )
    from keyboards.reply_kb import get_main_kb
    await callback.message.answer(text, parse_mode="HTML", reply_markup=get_main_kb())'''

    if old_block in text:
        text = text.replace(old_block, new_block)
        with open('handlers/user.py', 'w', encoding='utf-8') as f:
            f.write(text)
        print("Updated cb_check_subscription in user.py")
    else:
        print("Block not found in user.py!")

run()
