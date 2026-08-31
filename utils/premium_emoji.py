"""
Telegram Premium Emoji konstantalar va yordamchi funksiyalar.

USE_PREMIUM_EMOJI = True  → <tg-emoji> teglar ishlatiladi (default).
USE_PREMIUM_EMOJI = False → oddiy Unicode fallback ishlatiladi.
"""

import os

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  PREMIUM EMOJI REJIMI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

USE_PREMIUM_EMOJI: bool = os.getenv("USE_PREMIUM_EMOJI", "true").lower() == "true"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  PREMIUM EMOJI GENERATOR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def _pe(emoji_id: str, fallback: str = "") -> str:
    """Premium emoji yoki fallback qaytarish."""
    if USE_PREMIUM_EMOJI:
        return f'<tg-emoji emoji-id="{emoji_id}">{fallback}</tg-emoji>'
    return fallback


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  KINO VA KO'NGILOCHAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PE_MOVIE = _pe("5375464961822695044", "\U0001f3ac")
PE_POPCORN = _pe("5469903029144657419", "\U0001f37f")
PE_FIRE = _pe("5438356288197133913", "\U0001f525")
PE_TROPHY = _pe("5438485047021705795", "\U0001f3c6")
PE_STAR = _pe("5433653135799228968", "\u2b50")
PE_SPARKLE = _pe("5409008750893734809", "\u2728")
PE_CLAPPER = _pe("5375464961822695044", "\U0001f3ac")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  NAVIGATSIYA VA HARAKATLAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PE_SEARCH = _pe("5435957248314579621", "\U0001f50d")
PE_HOME = _pe("5472164874886846699", "\U0001f3e0")
PE_BACK = _pe("6323120985692177951", "\u25c0\ufe0f")
PE_FORWARD = _pe("5188217332748527444", "\u25b6\ufe0f")
PE_ADD = _pe("5465226866321268133", "\u2795")
PE_DELETE = _pe("5215484787325676090", "\U0001f5d1\ufe0f")
PE_DOWNLOAD = _pe("6323133642960799652", "\U0001f4e5")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  HOLAT INDIKATORLARI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PE_CHECK = _pe("5330115548900501467", "\u2705")
PE_CROSS = _pe("6323301979908998512", "\u274c")
PE_WARNING = _pe("5438491618321665691", "\u26a0\ufe0f")
PE_INFO = _pe("5438618057863893203", "\u2139\ufe0f")
PE_LOCK = _pe("5433811242135331842", "\U0001f512")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ADMIN VA TIZIM
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PE_GEAR = _pe("5438099401908192133", "\u2699\ufe0f")
PE_CHART = _pe("5438574962162043987", "\U0001f4ca")
PE_USER = _pe("5440603840288165037", "\U0001f464")
PE_USERS = _pe("5472055112702629499", "\U0001f465")
PE_SEND = _pe("6323395189289256377", "\U0001f4e4")
PE_CHANNEL = _pe("5334979955845507016", "\U0001f4e2")
PE_MEGAPHONE = _pe("5296369303661067030", "\U0001f4e3")
PE_CROWN = _pe("5440480175294810918", "\U0001f451")
PE_FOLDER = _pe("5258096772776991776", "\U0001f4c1")
PE_NUMBER = _pe("5438326064512275784", "#\ufe0f\u20e3")
PE_CLOCK = _pe("5373012449597335010", "\U0001f550")
PE_KEY = _pe("6174589325695521740", "\U0001f511")
PE_WAVE = _pe("5372926953978341366", "\U0001f44b")
PE_GLOBE = _pe("5438236364120298680", "\U0001f310")
PE_PIN = _pe("5433614747381538714", "\U0001f4cc")
PE_SHIELD = _pe("5372981976804366741", "\U0001f6e1\ufe0f")
PE_DIAMOND = _pe("5780405967527089720", "\U0001f48e")
PE_ROBOT = _pe("5371081166013078244", "\U0001f916")


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
