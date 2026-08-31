"""Reply klaviaturalar."""

from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)


def get_main_menu_kb() -> ReplyKeyboardMarkup:
    """Foydalanuvchi asosiy menyu."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="\u25c8 Kino qidirish"),
                KeyboardButton(text="\u2606 Mashhur kinolar"),
            ],
            [
                KeyboardButton(text="\u2737 Yangi kinolar"),
                KeyboardButton(text="\u25c7 Biz haqimizda"),
            ],
        ],
        resize_keyboard=True,
        input_field_placeholder="Kino kodini yuboring...",
    )


def get_admin_menu_kb() -> ReplyKeyboardMarkup:
    """Admin asosiy menyu (qo'shimcha Admin panel tugmasi)."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="\u2726 Admin panel"),
            ],
            [
                KeyboardButton(text="\u25c8 Kino qidirish"),
                KeyboardButton(text="\u2606 Mashhur kinolar"),
            ],
            [
                KeyboardButton(text="\u2737 Yangi kinolar"),
                KeyboardButton(text="\u25c7 Biz haqimizda"),
            ],
        ],
        resize_keyboard=True,
        input_field_placeholder="Kino kodini yuboring...",
    )


def get_cancel_kb() -> ReplyKeyboardMarkup:
    """Bekor qilish tugmasi."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="\u2717 Bekor qilish")],
        ],
        resize_keyboard=True,
    )


remove_kb = ReplyKeyboardRemove()
