import os

def run():
    with open('handlers/user.py', 'r', encoding='utf-8') as f:
        text = f.read()

    old_join = '''@router.chat_join_request()
async def approve_join_request(join_request: ChatJoinRequest, bot: Bot) -> None:
    """Maxfiy kanalga zayavka tashlaganlarni avtomat qabul qiladi."""
    try:
        await bot.approve_chat_join_request(
            chat_id=join_request.chat.id,
            user_id=join_request.from_user.id
        )
        await bot.send_message(
            chat_id=join_request.from_user.id,
            text=f"✅ <b>{join_request.chat.title}</b> kanaliga so'rovingiz qabul qilindi!\\nEndi botdan bemalol foydalanishingiz mumkin.",
            parse_mode="HTML"
        )
    except Exception:
        pass'''

    new_join = '''@router.chat_join_request()
async def handle_join_request(join_request: ChatJoinRequest, bot: Bot, db: Database) -> None:
    """Maxfiy kanalga zayavka tashlaganlarni bazaga saqlaydi va qabul qilmay turib ruxsat beradi."""
    try:
        await db.add_join_request(join_request.from_user.id, join_request.chat.id)
        await bot.send_message(
            chat_id=join_request.from_user.id,
            text=f"✅ <b>{join_request.chat.title}</b> kanaliga so'rovingiz yuborildi!\\nEndi botdan bemalol foydalanishingiz mumkin.",
            parse_mode="HTML"
        )
    except Exception as e:
        pass'''

    if old_join in text:
        text = text.replace(old_join, new_join)
        with open('handlers/user.py', 'w', encoding='utf-8') as f:
            f.write(text)
        print("Replaced in user.py")

run()
