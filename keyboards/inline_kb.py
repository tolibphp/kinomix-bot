"""Inline klaviaturalar - Foydalanuvchi va Admin uchun."""

from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  FOYDALANUVCHI KLAVIATURALARI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def get_subscription_kb(
    channels: list,
) -> InlineKeyboardMarkup:
    """Majburiy obuna kanallar klaviaturasi."""
    builder = InlineKeyboardBuilder()
    for ch in channels:
        username = ch["channel_username"] or ""
        title = ch["channel_title"] or username
        builder.row(
            InlineKeyboardButton(
                text=f"\u25b6 {title}",
                url=f"https://t.me/{username.lstrip('@')}",
            )
        )
    builder.row(
        InlineKeyboardButton(
            text="\u2713 Tekshirish",
            callback_data="check_subscription",
        )
    )
    return builder.as_markup()


def get_main_inline_kb() -> InlineKeyboardMarkup:
    """Asosiy inline menyu."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="\u25c8 Kino qidirish",
            callback_data="search_movie",
        ),
        InlineKeyboardButton(
            text="\u2606 Mashhurlar",
            callback_data="popular_movies",
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text="\u2737 Yangi kinolar",
            callback_data="recent_movies",
        ),
    )
    return builder.as_markup()


def get_movie_kb(code: str) -> InlineKeyboardMarkup:
    """Kino ko'rish tugmasi."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="\u25c8 Qidirish",
            callback_data="search_movie",
        ),
        InlineKeyboardButton(
            text="\u2606 Mashhurlar",
            callback_data="popular_movies",
        ),
    )
    return builder.as_markup()


def get_search_results_kb(
    movies: list, page: int = 0, per_page: int = 5
) -> InlineKeyboardMarkup:
    """Qidiruv natijalari klaviaturasi sahifalash bilan."""
    builder = InlineKeyboardBuilder()
    start = page * per_page
    end = start + per_page
    page_movies = movies[start:end]

    for movie in page_movies:
        builder.row(
            InlineKeyboardButton(
                text=f"\u25b8 {movie['title']} | {movie['code']}",
                callback_data=f"get_movie:{movie['code']}",
            )
        )

    nav_buttons: list[InlineKeyboardButton] = []
    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton(
                text="\u25c2 Oldingi",
                callback_data=f"search_page:{page - 1}",
            )
        )
    if end < len(movies):
        nav_buttons.append(
            InlineKeyboardButton(
                text="Keyingi \u25b8",
                callback_data=f"search_page:{page + 1}",
            )
        )
    if nav_buttons:
        builder.row(*nav_buttons)

    builder.row(
        InlineKeyboardButton(
            text="\u25c6 Bosh menyu",
            callback_data="main_menu",
        )
    )
    return builder.as_markup()


def get_popular_movies_kb(movies: list) -> InlineKeyboardMarkup:
    """Mashhur kinolar ro'yxati."""
    builder = InlineKeyboardBuilder()
    for i, movie in enumerate(movies, 1):
        views = movie["views"]
        builder.row(
            InlineKeyboardButton(
                text=f"{i}. {movie['title']}  \u2014  {views} ko'rish",
                callback_data=f"get_movie:{movie['code']}",
            )
        )
    builder.row(
        InlineKeyboardButton(
            text="\u25c6 Bosh menyu",
            callback_data="main_menu",
        )
    )
    return builder.as_markup()


def get_recent_movies_kb(movies: list) -> InlineKeyboardMarkup:
    """Yangi qo'shilgan kinolar."""
    builder = InlineKeyboardBuilder()
    for movie in movies:
        builder.row(
            InlineKeyboardButton(
                text=f"\u25b8 {movie['title']} | {movie['code']}",
                callback_data=f"get_movie:{movie['code']}",
            )
        )
    builder.row(
        InlineKeyboardButton(
            text="\u25c6 Bosh menyu",
            callback_data="main_menu",
        )
    )
    return builder.as_markup()


def get_back_kb() -> InlineKeyboardMarkup:
    """Orqaga tugmasi."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="\u25c2 Orqaga",
                    callback_data="main_menu",
                )
            ]
        ]
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ADMIN KLAVIATURALARI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def get_admin_panel_kb() -> InlineKeyboardMarkup:
    """Admin boshqaruv paneli."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="\u002b Kino qo'shish",
            callback_data="admin:add_movie",
        ),
        InlineKeyboardButton(
            text="\u00d7 Kino o'chirish",
            callback_data="admin:delete_movie",
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text="\u25a3 Kinolar ro'yxati",
            callback_data="admin:movie_list",
        ),
        InlineKeyboardButton(
            text="\u2261 Statistika",
            callback_data="admin:statistics",
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text="\u00bb Xabar yuborish",
            callback_data="admin:broadcast",
        ),
        InlineKeyboardButton(
            text="\u229a Kanallar",
            callback_data="admin:channels",
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text="\u25c6 Bosh menyu",
            callback_data="main_menu",
        )
    )
    return builder.as_markup()


def get_admin_confirm_kb(action: str) -> InlineKeyboardMarkup:
    """Tasdiqlash / Bekor qilish."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="\u2713 Tasdiqlash",
                    callback_data=f"confirm:{action}",
                ),
                InlineKeyboardButton(
                    text="\u2717 Bekor qilish",
                    callback_data="admin:cancel",
                ),
            ]
        ]
    )


def get_skip_caption_kb() -> InlineKeyboardMarkup:
    """Caption o'tkazib yuborish."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="\u25b8 O'tkazib yuborish",
                    callback_data="skip_caption",
                )
            ],
            [
                InlineKeyboardButton(
                    text="\u2717 Bekor qilish",
                    callback_data="admin:cancel",
                )
            ],
        ]
    )


def get_admin_back_kb() -> InlineKeyboardMarkup:
    """Admin panelga qaytish."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="\u25c2 Admin panel",
                    callback_data="admin:panel",
                ),
                InlineKeyboardButton(
                    text="\u2717 Bekor qilish",
                    callback_data="admin:cancel",
                ),
            ]
        ]
    )


def get_channel_management_kb(channels: list) -> InlineKeyboardMarkup:
    """Kanallarni boshqarish."""
    builder = InlineKeyboardBuilder()
    for ch in channels:
        username = ch["channel_username"] or str(ch["channel_id"])
        title = ch["channel_title"] or username
        builder.row(
            InlineKeyboardButton(
                text=f"\u2717 {title}",
                callback_data=f"remove_channel:{ch['channel_id']}",
            )
        )
    builder.row(
        InlineKeyboardButton(
            text="\u002b Kanal qo'shish",
            callback_data="admin:add_channel",
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="\u25c2 Admin panel",
            callback_data="admin:panel",
        )
    )
    return builder.as_markup()


def get_movie_list_kb(
    movies: list, page: int = 0, per_page: int = 8
) -> InlineKeyboardMarkup:
    """Admin kinolar ro'yxati sahifalash bilan."""
    builder = InlineKeyboardBuilder()
    start = page * per_page
    end = start + per_page
    page_movies = movies[start:end]

    for movie in page_movies:
        views = movie["views"]
        builder.row(
            InlineKeyboardButton(
                text=f"[{movie['code']}] {movie['title']}  ({views})",
                callback_data=f"admin:view_movie:{movie['code']}",
            )
        )

    nav_buttons: list[InlineKeyboardButton] = []
    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton(
                text="\u25c2 Oldingi",
                callback_data=f"admin:movie_page:{page - 1}",
            )
        )
    if end < len(movies):
        nav_buttons.append(
            InlineKeyboardButton(
                text="Keyingi \u25b8",
                callback_data=f"admin:movie_page:{page + 1}",
            )
        )
    if nav_buttons:
        builder.row(*nav_buttons)

    builder.row(
        InlineKeyboardButton(
            text="\u25c2 Admin panel",
            callback_data="admin:panel",
        )
    )
    return builder.as_markup()


def get_admin_movie_detail_kb(code: str) -> InlineKeyboardMarkup:
    """Admin kino tafsilotlari."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="\u00d7 O'chirish",
                    callback_data=f"admin:confirm_delete:{code}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="\u25c2 Ro'yxatga qaytish",
                    callback_data="admin:movie_list",
                )
            ],
        ]
    )


def get_confirm_delete_kb(code: str) -> InlineKeyboardMarkup:
    """O'chirishni tasdiqlash."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="\u2713 Ha, o'chirish",
                    callback_data=f"admin:do_delete:{code}",
                ),
                InlineKeyboardButton(
                    text="\u2717 Yo'q, bekor qilish",
                    callback_data="admin:movie_list",
                ),
            ]
        ]
    )
