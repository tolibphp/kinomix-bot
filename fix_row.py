import os

def fix_inline_kb():
    with open('keyboards/inline_kb.py', 'r', encoding='utf-8') as f:
        text = f.read()

    # Find the get_subscription_kb
    old_block = '''def get_subscription_kb(
    channels: list,
) -> InlineKeyboardMarkup:
    """Majburiy obuna kanallar klaviaturasi."""
    builder = InlineKeyboardBuilder()
    for ch in channels:
        username = ch.get("channel_username")'''

    new_block = '''def get_subscription_kb(
    channels: list,
) -> InlineKeyboardMarkup:
    """Majburiy obuna kanallar klaviaturasi."""
    builder = InlineKeyboardBuilder()
    for row in channels:
        ch = dict(row) if hasattr(row, "keys") else row
        username = ch.get("channel_username")'''

    if old_block in text:
        text = text.replace(old_block, new_block)
        with open('keyboards/inline_kb.py', 'w', encoding='utf-8') as f:
            f.write(text)
        print("Fixed inline_kb.py")
    else:
        print("Block not found in inline_kb.py")

def fix_middleware():
    with open('middlewares/subscription.py', 'r', encoding='utf-8') as f:
        text = f.read()

    old_block = '''        bot: Bot = data["bot"]
        not_subscribed: list[dict] = []

        for ch in channels:
            try:
                member = await bot.get_chat_member(
                    chat_id=ch["channel_id"], user_id=user.id
                )'''

    new_block = '''        bot: Bot = data["bot"]
        not_subscribed: list[dict] = []

        for row in channels:
            ch = dict(row) if hasattr(row, "keys") else row
            try:
                member = await bot.get_chat_member(
                    chat_id=ch["channel_id"], user_id=user.id
                )'''

    if old_block in text:
        text = text.replace(old_block, new_block)
        with open('middlewares/subscription.py', 'w', encoding='utf-8') as f:
            f.write(text)
        print("Fixed middleware.py")
    else:
        print("Block not found in middleware.py")

fix_inline_kb()
fix_middleware()
