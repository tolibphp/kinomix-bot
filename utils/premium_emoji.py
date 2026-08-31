"""
Telegram Premium Emoji konstantalar va yordamchi funksiyalar.

Premium emojilar faqat HTML parse_mode bilan xabar matnida ishlaydi.
Tugma (button) matnida HTML tahlil qilinmaydi.
"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  PREMIUM EMOJI GENERATOR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def _pe(emoji_id: str, fallback: str = "") -> str:
    """Premium emoji HTML tegini yaratish."""
    return f'<tg-emoji emoji-id="{emoji_id}">{fallback}</tg-emoji>'


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  KINO VA KO'NGILOCHAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PE_MOVIE = _pe("5368324170671202286", "\U0001f3ac")
PE_POPCORN = _pe("5373141891321699086", "\U0001f37f")
PE_FIRE = _pe("5372981976804190757", "\U0001f525")
PE_TROPHY = _pe("5371914108254406850", "\U0001f3c6")
PE_STAR = _pe("5373026167722876034", "\u2b50")
PE_SPARKLE = _pe("5368324170671202286", "\u2728")
PE_CLAPPER = _pe("5370889696386949886", "\U0001f3ac")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  NAVIGATSIYA VA HARAKATLAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PE_SEARCH = _pe("5372943360747110126", "\U0001f50d")
PE_HOME = _pe("5370900899890987847", "\U0001f3e0")
PE_BACK = _pe("5377437404078546699", "\u25c0\ufe0f")
PE_FORWARD = _pe("5372981976804190757", "\u25b6\ufe0f")
PE_ADD = _pe("5368324170671202286", "\u2795")
PE_DELETE = _pe("5377437404078546699", "\U0001f5d1\ufe0f")
PE_DOWNLOAD = _pe("5372981976804190757", "\U0001f4e5")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  HOLAT INDIKATORLARI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PE_CHECK = _pe("5372981976804190757", "\u2705")
PE_CROSS = _pe("5377437404078546699", "\u274c")
PE_WARNING = _pe("5373141891321699086", "\u26a0\ufe0f")
PE_INFO = _pe("5372981976804190757", "\u2139\ufe0f")
PE_LOCK = _pe("5377437404078546699", "\U0001f512")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ADMIN VA TIZIM
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PE_GEAR = _pe("5373026167722876034", "\u2699\ufe0f")
PE_CHART = _pe("5371914108254406850", "\U0001f4ca")
PE_USER = _pe("5370900899890987847", "\U0001f464")
PE_USERS = _pe("5370900899890987847", "\U0001f465")
PE_SEND = _pe("5372981976804190757", "\U0001f4e4")
PE_CHANNEL = _pe("5371914108254406850", "\U0001f4e2")
PE_MEGAPHONE = _pe("5373141891321699086", "\U0001f4e3")
PE_CROWN = _pe("5368324170671202286", "\U0001f451")
PE_FOLDER = _pe("5371914108254406850", "\U0001f4c1")
PE_NUMBER = _pe("5372981976804190757", "#\ufe0f\u20e3")
PE_CLOCK = _pe("5373026167722876034", "\U0001f550")
PE_KEY = _pe("5368324170671202286", "\U0001f511")
PE_WAVE = _pe("5368324170671202286", "\U0001f44b")
PE_GLOBE = _pe("5371914108254406850", "\U0001f310")
PE_PIN = _pe("5373026167722876034", "\U0001f4cc")
PE_SHIELD = _pe("5368324170671202286", "\U0001f6e1\ufe0f")
PE_DIAMOND = _pe("5373141891321699086", "\U0001f48e")
PE_ROBOT = _pe("5372981976804190757", "\U0001f916")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  YORDAMCHI FUNKSIYALAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def is_admin(user_id: int, admin_ids: list[int]) -> bool:
    """Foydalanuvchi admin ekanligini tekshirish."""
    return user_id in admin_ids


def format_movie_caption(
    title: str, code: str, caption: str | None = None
) -> str:
    """Kino uchun chiroyli caption yaratish."""
    text = (
        f"{PE_CLAPPER} <b>{title}</b>\n"
        f"{'━' * 22}\n\n"
        f"{PE_NUMBER} <b>Kod:</b> <code>{code}</code>\n"
    )
    if caption:
        text += f"\n{PE_PIN} {caption}\n"

    text += (
        f"\n{'━' * 22}\n"
        f"{PE_POPCORN} <i>Yoqimli tomosha tilaymiz!</i>"
    )
    return text


def format_number(num: int) -> str:
    """Raqamni ming ajratgich bilan formatlash."""
    return f"{num:,}".replace(",", " ")
