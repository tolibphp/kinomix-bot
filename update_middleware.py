import os

def run():
    with open('middlewares/subscription.py', 'r', encoding='utf-8') as f:
        text = f.read()

    old_block = '''            try:
                member = await bot.get_chat_member(
                    chat_id=ch["channel_id"], user_id=user.id
                )
                if member.status in ("left", "kicked"):
                    not_subscribed.append(
                        {
                            "channel_id": ch["channel_id"],
                            "channel_username": ch.get("channel_username"),
                            "channel_title": ch.get("channel_title"),
                            "invite_link": ch.get("invite_link"),
                        }
                    )
            except Exception:
                # Agar user topilmasa yoki xatolik bersa, demak obuna emas!
                not_subscribed.append(
                    {
                        "channel_id": ch["channel_id"],
                        "channel_username": ch.get("channel_username"),
                        "channel_title": ch.get("channel_title"),
                        "invite_link": ch.get("invite_link"),
                    }
                )'''

    new_block = '''            try:
                member = await bot.get_chat_member(
                    chat_id=ch["channel_id"], user_id=user.id
                )
                if member.status in ("left", "kicked"):
                    # Zayavka tashlaganligini tekshiramiz
                    has_req = await self.db.has_join_request(user.id, ch["channel_id"])
                    if not has_req:
                        not_subscribed.append(
                            {
                                "channel_id": ch["channel_id"],
                                "channel_username": ch.get("channel_username"),
                                "channel_title": ch.get("channel_title"),
                                "invite_link": ch.get("invite_link"),
                            }
                        )
            except Exception:
                # Agar user topilmasa yoki xatolik bersa, demak obuna emas!
                # Lekin zayavka tashlagan bo'lsa o'tkazib yuboramiz
                has_req = await self.db.has_join_request(user.id, ch["channel_id"])
                if not has_req:
                    not_subscribed.append(
                        {
                            "channel_id": ch["channel_id"],
                            "channel_username": ch.get("channel_username"),
                            "channel_title": ch.get("channel_title"),
                            "invite_link": ch.get("invite_link"),
                        }
                    )'''

    if old_block in text:
        text = text.replace(old_block, new_block)
        with open('middlewares/subscription.py', 'w', encoding='utf-8') as f:
            f.write(text)
        print("Replaced in middleware")

run()
