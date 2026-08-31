"""Admin handlerlari."""

from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import ADMIN_IDS
from database.db import Database
from keyboards.inline_kb import (
    get_admin_back_kb,
    get_admin_confirm_kb,
    get_admin_movie_detail_kb,
    get_admin_panel_kb,
    get_channel_management_kb,
    get_confirm_delete_kb,
    get_main_inline_kb,
    get_movie_list_kb,
    get_skip_caption_kb,
)
from keyboards.reply_kb import get_admin_menu_kb, get_cancel_kb
from states.states import (
    AddChannelStates,
    AddMovieStates,
    BroadcastStates,
    DeleteMovieStates,
    ChannelPostStates,
)
from utils.premium_emoji import (
    PE_ADD,
    PE_CHANNEL,
    PE_CHART,
    PE_CHECK,
    PE_CLOCK,
    PE_CLAPPER,
    PE_CROSS,
    PE_CROWN,
    PE_DELETE,
    PE_FIRE,
    PE_FOLDER,
    PE_GLOBE,
    PE_HOME,
    PE_INFO,
    PE_KEY,
    PE_MEGAPHONE,
    PE_MOVIE,
    PE_NUMBER,
    PE_PIN,
    PE_SEND,
    PE_SPARKLE,
    PE_STAR,
    PE_USER,
    PE_USERS,
    PE_WARNING,
    format_movie_caption,
    format_number,
)

logger = logging.getLogger(__name__)

router = Router(name="admin")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ADMIN FILTR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def _is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ADMIN PANEL
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


from aiogram.filters import CommandStart, StateFilter

@router.message(CommandStart(), StateFilter("*"))
async def admin_cmd_start(message: Message, db: Database, state: FSMContext) -> None:
    """FSM holatidan qat'i nazar /start buyrug'ini ushlab olish."""
    await state.clear()
    from handlers.user import cmd_start
    await cmd_start(message, db, state)


@router.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext) -> None:
    if not _is_admin(message.from_user.id):
        return
    await state.clear()
    await _show_admin_panel(message)


@router.message(F.text.contains("Admin panel"))
async def reply_admin_panel(message: Message, state: FSMContext) -> None:
    if not _is_admin(message.from_user.id):
        return
    await state.clear()
    await _show_admin_panel(message)


@router.callback_query(F.data == "admin:panel")
async def cb_admin_panel(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q", show_alert=True)
        return
    await state.clear()
    text = (
        f"{PE_CROWN} <b>Admin boshqaruv paneli</b>\n"
        f"{'━' * 28}\n\n"
        f"{PE_INFO} Kerakli bo'limni tanlang:"
    )
    await callback.message.edit_text(
        text, reply_markup=get_admin_panel_kb(), parse_mode="HTML"
    )
    await callback.answer()


async def _show_admin_panel(message: Message) -> None:
    text = (
        f"{PE_CROWN} <b>Admin boshqaruv paneli</b>\n"
        f"{'━' * 28}\n\n"
        f"{PE_INFO} Kerakli bo'limni tanlang:"
    )
    await message.answer(
        text, reply_markup=get_admin_panel_kb(), parse_mode="HTML"
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  BEKOR QILISH (Admin FSM)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@router.callback_query(F.data == "admin:cancel")
async def cb_admin_cancel(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        return
    await state.clear()

    text = f"{PE_CHECK} <b>Bekor qilindi</b>"
    await callback.message.edit_text(text, parse_mode="HTML")

    # Admin panelni qayta ko'rsatish
    panel_text = (
        f"{PE_CROWN} <b>Admin boshqaruv paneli</b>\n"
        f"{'━' * 28}\n\n"
        f"{PE_INFO} Kerakli bo'limni tanlang:"
    )
    await callback.message.answer(
        panel_text, reply_markup=get_admin_panel_kb(), parse_mode="HTML"
    )
    # Reply keyboard'ni qaytarish
    await callback.message.answer(
        f"{PE_HOME} <b>Menyu yangilandi</b>",
        reply_markup=get_admin_menu_kb(),
        parse_mode="HTML",
    )
    await callback.answer()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  KINO QO'SHISH
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@router.callback_query(F.data == "admin:add_movie")
async def cb_add_movie_start(
    callback: CallbackQuery, state: FSMContext
) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q", show_alert=True)
        return

    await state.set_state(AddMovieStates.waiting_for_code)
    text = (
        f"{PE_ADD} <b>Yangi kino qo'shish</b>\n"
        f"{'━' * 28}\n\n"
        f"{PE_NUMBER} <b>1-qadam:</b> Kino kodini yuboring\n\n"
        f"{PE_INFO} <i>Masalan:</i> <code>1234</code>"
    )
    await callback.message.edit_text(
        text, reply_markup=get_admin_back_kb(), parse_mode="HTML"
    )
    # Cancel reply keyboard
    await callback.message.answer(
        f"{PE_KEY} Kino kodini yuboring:",
        reply_markup=get_cancel_kb(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.message(AddMovieStates.waiting_for_code)
async def process_movie_code(
    message: Message, db: Database, state: FSMContext
) -> None:
    if not _is_admin(message.from_user.id):
        return

    # Bekor qilish
    if message.text and "Bekor qilish" in message.text:
        await state.clear()
        await message.answer(
            f"{PE_CHECK} <b>Bekor qilindi</b>",
            reply_markup=get_admin_menu_kb(),
            parse_mode="HTML",
        )
        await _show_admin_panel(message)
        return

    code = message.text.strip() if message.text else ""
    if not code:
        await message.answer(
            f"{PE_CROSS} Iltimos, kino kodini matn ko'rinishida yuboring.",
            parse_mode="HTML",
        )
        return

    # Tekshirish: bu kod allaqachon mavjudmi
    existing = await db.get_movie_by_code(code)
    if existing:
        text = (
            f"{PE_WARNING} <b>Bu kod band!</b>\n\n"
            f"{PE_INFO} <code>{code}</code> kodli kino allaqachon mavjud:\n"
            f"{PE_MOVIE} {existing['title']}\n\n"
            f"{PE_SPARKLE} Boshqa kod yuboring."
        )
        await message.answer(text, parse_mode="HTML")
        return

    await state.update_data(code=code)
    await state.set_state(AddMovieStates.waiting_for_title)

    text = (
        f"{PE_CHECK} Kod: <code>{code}</code>\n\n"
        f"{PE_CLAPPER} <b>2-qadam:</b> Kino nomini yuboring\n\n"
        f"{PE_INFO} <i>Masalan:</i> <code>Matrix 1999</code>"
    )
    await message.answer(text, parse_mode="HTML")


@router.message(AddMovieStates.waiting_for_title)
async def process_movie_title(
    message: Message, state: FSMContext
) -> None:
    if not _is_admin(message.from_user.id):
        return

    if message.text and "Bekor qilish" in message.text:
        await state.clear()
        await message.answer(
            f"{PE_CHECK} <b>Bekor qilindi</b>",
            reply_markup=get_admin_menu_kb(),
            parse_mode="HTML",
        )
        await _show_admin_panel(message)
        return

    title = message.text.strip() if message.text else ""
    if not title:
        await message.answer(
            f"{PE_CROSS} Iltimos, kino nomini matn ko'rinishida yuboring.",
            parse_mode="HTML",
        )
        return

    await state.update_data(title=title)
    await state.set_state(AddMovieStates.waiting_for_file)

    text = (
        f"{PE_CHECK} Nomi: <b>{title}</b>\n\n"
        f"{PE_MOVIE} <b>3-qadam:</b> Kino faylini yuboring\n\n"
        f"{PE_INFO} Video yoki dokument sifatida yuborishingiz mumkin."
    )
    await message.answer(
        text, reply_markup=get_admin_back_kb(), parse_mode="HTML"
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  KANALGA POST YUBORISH
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@router.callback_query(F.data == "admin:channel_post")
async def cb_admin_channel_post(callback: CallbackQuery, db: Database, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        return
    channels = await db.get_channels()
    if not channels:
        await callback.answer("Bazada kanallar yo'q! Oldin kanal qo'shing.", show_alert=True)
        return
    await state.set_state(ChannelPostStates.waiting_for_channel)
    from keyboards.inline_kb import get_post_channels_kb
    text = f"{PE_CHANNEL} <b>Qaysi kanalga post yuboramiz?</b>"
    await callback.message.edit_text(text, reply_markup=get_post_channels_kb(channels), parse_mode="HTML")
    await callback.answer()


@router.callback_query(ChannelPostStates.waiting_for_channel, F.data.startswith("post_channel:"))
async def cb_post_channel_selected(callback: CallbackQuery, state: FSMContext) -> None:
    channel_id = int(callback.data.split(":")[1])
    await state.update_data(post_channel_id=channel_id)
    await state.set_state(ChannelPostStates.waiting_for_code)
    text = (
        f"{PE_MOVIE} <b>Kino kodini yuboring</b>\n\n"
        f"{PE_INFO} Bu kod postdagi tugmani bosganda ishlaydi."
    )
    from keyboards.inline_kb import get_admin_back_kb
    await callback.message.edit_text(text, reply_markup=get_admin_back_kb(), parse_mode="HTML")
    await callback.answer()


@router.message(ChannelPostStates.waiting_for_code, F.text)
async def post_code_received(message: Message, state: FSMContext) -> None:
    code = message.text.strip()
    await state.update_data(post_code=code)
    await state.set_state(ChannelPostStates.waiting_for_media)
    text = (
        f"{PE_CLAPPER} <b>Kino uchun rasm yoki qisqa video yuboring</b>"
    )
    from keyboards.inline_kb import get_admin_back_kb
    await message.answer(text, reply_markup=get_admin_back_kb(), parse_mode="HTML")


@router.message(ChannelPostStates.waiting_for_media, F.photo | F.video | F.document)
async def post_media_received(message: Message, state: FSMContext) -> None:
    if message.photo:
        file_id = message.photo[-1].file_id
        file_type = "photo"
    elif message.video:
        file_id = message.video.file_id
        file_type = "video"
    else:
        file_id = message.document.file_id
        file_type = "document"

    await state.update_data(post_media_id=file_id, post_media_type=file_type)
    await state.set_state(ChannelPostStates.waiting_for_caption)
    text = (
        f"{PE_PIN} <b>Kino haqida qisqa ma'lumot (caption) yozing</b>"
    )
    from keyboards.inline_kb import get_admin_back_kb
    await message.answer(text, reply_markup=get_admin_back_kb(), parse_mode="HTML")


@router.message(ChannelPostStates.waiting_for_caption, F.text)
async def post_caption_received(message: Message, state: FSMContext, bot: Bot) -> None:
    caption = message.text
    data = await state.get_data()
    channel_id = data["post_channel_id"]
    code = data["post_code"]
    media_id = data["post_media_id"]
    media_type = data["post_media_type"]
    await state.clear()

    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    from utils.premium_emoji import ID_SEARCH
    
    bot_info = await bot.get_me()
    url = f"https://t.me/{bot_info.username}?start={code}"
    
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=" Kinoni ko'rish",
                    url=url,
                    icon_custom_emoji_id=ID_SEARCH,
                    style="success"
                )
            ]
        ]
    )

    try:
        if media_type == "photo":
            await bot.send_photo(chat_id=channel_id, photo=media_id, caption=caption, reply_markup=kb, parse_mode="HTML")
        elif media_type == "video":
            await bot.send_video(chat_id=channel_id, video=media_id, caption=caption, reply_markup=kb, parse_mode="HTML")
        else:
            await bot.send_document(chat_id=channel_id, document=media_id, caption=caption, reply_markup=kb, parse_mode="HTML")
        
        await message.answer(f"{PE_CHECK} <b>Post muvaffaqiyatli kanalga yuborildi!</b>", parse_mode="HTML")
        await _show_admin_panel(message)
    except Exception as e:
        await message.answer(f"{PE_CROSS} Xatolik: {e}", parse_mode="HTML")


@router.message(AddMovieStates.waiting_for_file, F.video)
async def process_movie_file_video(
    message: Message, state: FSMContext
) -> None:
    if not _is_admin(message.from_user.id):
        return

    await state.update_data(
        file_id=message.video.file_id, file_type="video"
    )
    await state.set_state(AddMovieStates.waiting_for_caption)

    text = (
        f"{PE_CHECK} Fayl qabul qilindi!\n\n"
        f"{PE_INFO} <b>4-qadam:</b> Caption yozing yoki o'tkazib yuboring."
    )
    await message.answer(
        text, reply_markup=get_skip_caption_kb(), parse_mode="HTML"
    )


@router.message(AddMovieStates.waiting_for_file, F.document)
async def process_movie_file_document(
    message: Message, state: FSMContext
) -> None:
    if not _is_admin(message.from_user.id):
        return

    await state.update_data(
        file_id=message.document.file_id, file_type="document"
    )
    await state.set_state(AddMovieStates.waiting_for_caption)

    text = (
        f"{PE_CHECK} Fayl qabul qilindi!\n\n"
        f"{PE_INFO} <b>4-qadam:</b> Caption yozing yoki o'tkazib yuboring."
    )
    await message.answer(
        text, reply_markup=get_skip_caption_kb(), parse_mode="HTML"
    )


@router.message(AddMovieStates.waiting_for_file, F.animation)
async def process_movie_file_animation(
    message: Message, state: FSMContext
) -> None:
    if not _is_admin(message.from_user.id):
        return

    await state.update_data(
        file_id=message.animation.file_id, file_type="animation"
    )
    await state.set_state(AddMovieStates.waiting_for_caption)

    text = (
        f"{PE_CHECK} Fayl qabul qilindi!\n\n"
        f"{PE_INFO} <b>4-qadam:</b> Caption yozing yoki o'tkazib yuboring."
    )
    await message.answer(
        text, reply_markup=get_skip_caption_kb(), parse_mode="HTML"
    )


@router.message(AddMovieStates.waiting_for_file)
async def process_movie_file_invalid(message: Message) -> None:
    if not _is_admin(message.from_user.id):
        return

    if message.text and "Bekor qilish" in message.text:
        return  # cancel handler handles this

    text = (
        f"{PE_CROSS} <b>Noto'g'ri format</b>\n\n"
        f"{PE_INFO} Iltimos, video yoki dokument yuboring."
    )
    await message.answer(text, parse_mode="HTML")


@router.callback_query(
    F.data == "skip_caption",
    AddMovieStates.waiting_for_caption,
)
async def cb_skip_caption(
    callback: CallbackQuery, db: Database, state: FSMContext
) -> None:
    if not _is_admin(callback.from_user.id):
        return
    await _save_movie(callback, db, state, caption=None)


@router.message(AddMovieStates.waiting_for_caption)
async def process_movie_caption(
    message: Message, db: Database, state: FSMContext
) -> None:
    if not _is_admin(message.from_user.id):
        return

    if message.text and "Bekor qilish" in message.text:
        await state.clear()
        await message.answer(
            f"{PE_CHECK} <b>Bekor qilindi</b>",
            reply_markup=get_admin_menu_kb(),
            parse_mode="HTML",
        )
        await _show_admin_panel(message)
        return

    caption = message.text.strip() if message.text else None
    await _save_movie_from_message(message, db, state, caption)


async def _save_movie(
    callback: CallbackQuery,
    db: Database,
    state: FSMContext,
    caption: str | None,
) -> None:
    data = await state.get_data()
    code = data["code"]
    title = data["title"]
    file_id = data["file_id"]
    file_type = data["file_type"]

    success = await db.add_movie(
        code=code,
        title=title,
        file_id=file_id,
        file_type=file_type,
        caption=caption,
        added_by=callback.from_user.id,
    )
    await state.clear()

    if success:
        text = (
            f"{PE_CHECK} <b>Kino muvaffaqiyatli qo'shildi!</b>\n"
            f"{'━' * 28}\n\n"
            f"{PE_MOVIE} <b>{title}</b>\n"
            f"{PE_NUMBER} Kod: <code>{code}</code>\n"
            f"{PE_STAR} Turi: {file_type}\n"
        )
        if caption:
            text += f"{PE_INFO} Caption: {caption}\n"
    else:
        text = (
            f"{PE_CROSS} <b>Xatolik!</b>\n\n"
            f"{PE_WARNING} Kino qo'shishda muammo yuz berdi.\n"
            f"Bu kod allaqachon mavjud bo'lishi mumkin."
        )

    await callback.message.edit_text(text, parse_mode="HTML")
    await callback.message.answer(
        f"{PE_HOME} <b>Menyu</b>",
        reply_markup=get_admin_menu_kb(),
        parse_mode="HTML",
    )
    await _show_admin_panel(callback.message)
    await callback.answer()


async def _save_movie_from_message(
    message: Message,
    db: Database,
    state: FSMContext,
    caption: str | None,
) -> None:
    data = await state.get_data()
    code = data["code"]
    title = data["title"]
    file_id = data["file_id"]
    file_type = data["file_type"]

    success = await db.add_movie(
        code=code,
        title=title,
        file_id=file_id,
        file_type=file_type,
        caption=caption,
        added_by=message.from_user.id,
    )
    await state.clear()

    if success:
        text = (
            f"{PE_CHECK} <b>Kino muvaffaqiyatli qo'shildi!</b>\n"
            f"{'━' * 28}\n\n"
            f"{PE_MOVIE} <b>{title}</b>\n"
            f"{PE_NUMBER} Kod: <code>{code}</code>\n"
            f"{PE_STAR} Turi: {file_type}\n"
        )
        if caption:
            text += f"{PE_INFO} Caption: {caption}\n"
    else:
        text = (
            f"{PE_CROSS} <b>Xatolik!</b>\n\n"
            f"{PE_WARNING} Kino qo'shishda muammo yuz berdi."
        )

    await message.answer(
        text, reply_markup=get_admin_menu_kb(), parse_mode="HTML"
    )
    await _show_admin_panel(message)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  KINO O'CHIRISH
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@router.callback_query(F.data == "admin:delete_movie")
async def cb_delete_movie_start(
    callback: CallbackQuery, state: FSMContext
) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q", show_alert=True)
        return

    await state.set_state(DeleteMovieStates.waiting_for_code)
    text = (
        f"{PE_DELETE} <b>Kino o'chirish</b>\n"
        f"{'━' * 28}\n\n"
        f"{PE_NUMBER} O'chirmoqchi bo'lgan kino kodini yuboring:"
    )
    await callback.message.edit_text(
        text, reply_markup=get_admin_back_kb(), parse_mode="HTML"
    )
    await callback.message.answer(
        f"{PE_KEY} Kino kodini yuboring:",
        reply_markup=get_cancel_kb(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.message(DeleteMovieStates.waiting_for_code)
async def process_delete_code(
    message: Message, db: Database, state: FSMContext
) -> None:
    if not _is_admin(message.from_user.id):
        return

    if message.text and "Bekor qilish" in message.text:
        await state.clear()
        await message.answer(
            f"{PE_CHECK} <b>Bekor qilindi</b>",
            reply_markup=get_admin_menu_kb(),
            parse_mode="HTML",
        )
        await _show_admin_panel(message)
        return

    code = message.text.strip() if message.text else ""
    if not code:
        await message.answer(
            f"{PE_CROSS} Kino kodini yuboring.", parse_mode="HTML"
        )
        return

    movie = await db.get_movie_by_code(code)
    if not movie:
        text = (
            f"{PE_CROSS} <code>{code}</code> kodli kino topilmadi.\n"
            f"{PE_INFO} Boshqa kod yuboring."
        )
        await message.answer(text, parse_mode="HTML")
        return

    await state.clear()
    text = (
        f"{PE_WARNING} <b>Kinoni o'chirmoqchimisiz?</b>\n"
        f"{'━' * 28}\n\n"
        f"{PE_MOVIE} <b>{movie['title']}</b>\n"
        f"{PE_NUMBER} Kod: <code>{movie['code']}</code>\n"
        f"{PE_FIRE} Ko'rishlar: {format_number(movie['views'])}\n"
    )
    await message.answer(
        text,
        reply_markup=get_confirm_delete_kb(code),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("admin:confirm_delete:"))
async def cb_confirm_delete(callback: CallbackQuery) -> None:
    if not _is_admin(callback.from_user.id):
        return
    code = callback.data.split(":", 2)[2]
    text = (
        f"{PE_WARNING} <b>Rostdan o'chirmoqchimisiz?</b>\n\n"
        f"{PE_INFO} Kod: <code>{code}</code>\n"
        f"{PE_DELETE} Bu amalni qaytarib bo'lmaydi!"
    )
    await callback.message.edit_text(
        text,
        reply_markup=get_confirm_delete_kb(code),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("admin:do_delete:"))
async def cb_do_delete(
    callback: CallbackQuery, db: Database
) -> None:
    if not _is_admin(callback.from_user.id):
        return
    code = callback.data.split(":", 2)[2]
    success = await db.delete_movie(code)

    if success:
        text = (
            f"{PE_CHECK} <b>Kino o'chirildi!</b>\n\n"
            f"{PE_NUMBER} <code>{code}</code> kodli kino bazadan olib tashlandi."
        )
    else:
        text = f"{PE_CROSS} <b>Kino topilmadi yoki o'chirib bo'lmadi</b>"

    await callback.message.edit_text(text, parse_mode="HTML")
    await _show_admin_panel(callback.message)
    await callback.answer()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  KINOLAR RO'YXATI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@router.callback_query(F.data == "admin:movie_list")
async def cb_movie_list(
    callback: CallbackQuery, db: Database
) -> None:
    if not _is_admin(callback.from_user.id):
        return

    movies = await db.get_all_movies(limit=200)
    if not movies:
        text = (
            f"{PE_INFO} <b>Kinolar ro'yxati bo'sh</b>\n\n"
            f"{PE_ADD} Yangi kino qo'shish uchun tugmani bosing."
        )
        await callback.message.edit_text(
            text, reply_markup=get_admin_panel_kb(), parse_mode="HTML"
        )
        await callback.answer()
        return

    text = (
        f"{PE_FOLDER} <b>Kinolar ro'yxati</b>\n"
        f"{'━' * 28}\n\n"
        f"{PE_MOVIE} Jami: <b>{format_number(len(movies))}</b> ta kino"
    )
    await callback.message.edit_text(
        text,
        reply_markup=get_movie_list_kb(movies),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("admin:movie_page:"))
async def cb_movie_page(
    callback: CallbackQuery, db: Database
) -> None:
    if not _is_admin(callback.from_user.id):
        return
    page = int(callback.data.split(":", 2)[2])
    movies = await db.get_all_movies(limit=200)

    text = (
        f"{PE_FOLDER} <b>Kinolar ro'yxati</b>\n"
        f"{'━' * 28}\n\n"
        f"{PE_MOVIE} Jami: <b>{format_number(len(movies))}</b> ta kino\n"
        f"{PE_INFO} Sahifa: {page + 1}"
    )
    await callback.message.edit_text(
        text,
        reply_markup=get_movie_list_kb(movies, page),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("admin:view_movie:"))
async def cb_view_movie(
    callback: CallbackQuery, db: Database
) -> None:
    if not _is_admin(callback.from_user.id):
        return
    code = callback.data.split(":", 2)[2]
    movie = await db.get_movie_by_code(code)

    if not movie:
        await callback.answer("Kino topilmadi", show_alert=True)
        return

    text = (
        f"{PE_MOVIE} <b>Kino tafsilotlari</b>\n"
        f"{'━' * 28}\n\n"
        f"{PE_CLAPPER} <b>{movie['title']}</b>\n\n"
        f"{PE_NUMBER} Kod: <code>{movie['code']}</code>\n"
        f"{PE_STAR} Turi: {movie['file_type']}\n"
        f"{PE_FIRE} Ko'rishlar: {format_number(movie['views'])}\n"
        f"{PE_CLOCK} Qo'shilgan: {movie['added_at']}\n"
    )
    if movie["caption"]:
        text += f"{PE_INFO} Caption: {movie['caption']}\n"

    await callback.message.edit_text(
        text,
        reply_markup=get_admin_movie_detail_kb(code),
        parse_mode="HTML",
    )
    await callback.answer()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  STATISTIKA
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@router.callback_query(F.data == "admin:statistics")
async def cb_statistics(
    callback: CallbackQuery, db: Database
) -> None:
    if not _is_admin(callback.from_user.id):
        return

    user_count = await db.get_user_count()
    movie_count = await db.get_movie_count()
    total_views = await db.get_total_views()
    today_users = await db.get_today_users()
    channels = await db.get_channels()

    text = (
        f"{PE_CHART} <b>Bot statistikasi</b>\n"
        f"{'━' * 28}\n\n"
        f"{PE_USERS} <b>Foydalanuvchilar:</b>\n"
        f"  {PE_USER} Jami: <b>{format_number(user_count)}</b>\n"
        f"  {PE_SPARKLE} Bugun: <b>{format_number(today_users)}</b>\n\n"
        f"{PE_MOVIE} <b>Kinolar:</b>\n"
        f"  {PE_FOLDER} Jami: <b>{format_number(movie_count)}</b>\n"
        f"  {PE_FIRE} Umumiy ko'rishlar: <b>{format_number(total_views)}</b>\n\n"
        f"{PE_CHANNEL} <b>Kanallar:</b> {len(channels)} ta\n"
        f"{'━' * 28}"
    )
    await callback.message.edit_text(
        text, reply_markup=get_admin_panel_kb(), parse_mode="HTML"
    )
    await callback.answer()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  XABAR YUBORISH (BROADCAST)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@router.callback_query(F.data == "admin:broadcast")
async def cb_broadcast_start(
    callback: CallbackQuery, state: FSMContext
) -> None:
    if not _is_admin(callback.from_user.id):
        return

    await state.set_state(BroadcastStates.waiting_for_message)
    text = (
        f"{PE_MEGAPHONE} <b>Xabar yuborish</b>\n"
        f"{'━' * 28}\n\n"
        f"{PE_INFO} Barcha foydalanuvchilarga yuboriladigan "
        f"xabarni yozing.\n\n"
        f"{PE_SEND} Matn, rasm, video yoki boshqa kontent "
        f"yuborishingiz mumkin."
    )
    await callback.message.edit_text(
        text, reply_markup=get_admin_back_kb(), parse_mode="HTML"
    )
    await callback.message.answer(
        f"{PE_SEND} Xabarni yuboring:",
        reply_markup=get_cancel_kb(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.message(BroadcastStates.waiting_for_message)
async def process_broadcast_message(
    message: Message, state: FSMContext
) -> None:
    if not _is_admin(message.from_user.id):
        return

    if message.text and "Bekor qilish" in message.text:
        await state.clear()
        await message.answer(
            f"{PE_CHECK} <b>Bekor qilindi</b>",
            reply_markup=get_admin_menu_kb(),
            parse_mode="HTML",
        )
        await _show_admin_panel(message)
        return

    # Xabarni saqlash
    await state.update_data(broadcast_message_id=message.message_id)
    await state.set_state(BroadcastStates.confirm)

    text = (
        f"{PE_WARNING} <b>Xabarni yuborishni tasdiqlaysizmi?</b>\n"
        f"{'━' * 28}\n\n"
        f"{PE_INFO} Yuqoridagi xabar barcha foydalanuvchilarga "
        f"yuboriladi."
    )
    await message.answer(
        text,
        reply_markup=get_admin_confirm_kb("broadcast"),
        parse_mode="HTML",
    )


@router.callback_query(
    F.data == "confirm:broadcast",
    BroadcastStates.confirm,
)
async def cb_confirm_broadcast(
    callback: CallbackQuery, db: Database, bot: Bot, state: FSMContext
) -> None:
    if not _is_admin(callback.from_user.id):
        return

    data = await state.get_data()
    msg_id = data.get("broadcast_message_id")
    await state.clear()

    user_ids = await db.get_all_user_ids()
    total = len(user_ids)

    text = (
        f"{PE_SEND} <b>Xabar yuborilmoqda...</b>\n\n"
        f"{PE_USERS} Jami: {format_number(total)} ta foydalanuvchi"
    )
    status_msg = await callback.message.edit_text(text, parse_mode="HTML")

    success = 0
    failed = 0

    for user_id in user_ids:
        try:
            await bot.copy_message(
                chat_id=user_id,
                from_chat_id=callback.from_user.id,
                message_id=msg_id,
            )
            success += 1
        except Exception:
            failed += 1

        # Telegram rate-limit'dan himoya
        if (success + failed) % 30 == 0:
            await asyncio.sleep(1.5)

    text = (
        f"{PE_CHECK} <b>Xabar yuborildi!</b>\n"
        f"{'━' * 28}\n\n"
        f"{PE_CHECK} Muvaffaqiyatli: <b>{format_number(success)}</b>\n"
        f"{PE_CROSS} Xatolik: <b>{format_number(failed)}</b>\n"
        f"{PE_USERS} Jami: <b>{format_number(total)}</b>"
    )
    await status_msg.edit_text(text, parse_mode="HTML")
    await _show_admin_panel(callback.message)
    await callback.answer()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  KANAL BOSHQARUVI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@router.callback_query(F.data == "admin:channels")
async def cb_channels(
    callback: CallbackQuery, db: Database
) -> None:
    if not _is_admin(callback.from_user.id):
        return

    channels = await db.get_channels()
    text = (
        f"{PE_CHANNEL} <b>Kanallar boshqaruvi</b>\n"
        f"{'━' * 28}\n\n"
    )
    if channels:
        text += f"{PE_INFO} Majburiy obuna kanallari: <b>{len(channels)}</b> ta\n\n"
        text += f"{PE_DELETE} O'chirish uchun kanal nomini bosing."
    else:
        text += f"{PE_INFO} Hozircha hech qanday kanal qo'shilmagan."

    await callback.message.edit_text(
        text,
        reply_markup=get_channel_management_kb(channels),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "admin:add_channel")
async def cb_add_channel(
    callback: CallbackQuery, state: FSMContext
) -> None:
    if not _is_admin(callback.from_user.id):
        return

    await state.set_state(AddChannelStates.waiting_for_channel)
    text = (
        f"{PE_ADD} <b>Kanal qo'shish</b>\n"
        f"{'━' * 28}\n\n"
        f"{PE_INFO} Kanaldagi istalgan xabarni shu botga forward qiling.\n\n"
        f"{PE_WARNING} <b>Eslatma:</b> Bot kanalda admin bo'lishi kerak!"
    )
    await callback.message.edit_text(
        text, reply_markup=get_admin_back_kb(), parse_mode="HTML"
    )
    await callback.message.answer(
        f"{PE_CHANNEL} Kanal xabarini forward qiling:",
        reply_markup=get_cancel_kb(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.message(AddChannelStates.waiting_for_channel)
async def process_add_channel(
    message: Message, db: Database, bot: Bot, state: FSMContext
) -> None:
    if not _is_admin(message.from_user.id):
        return

    if message.text and "Bekor qilish" in message.text:
        await state.clear()
        await message.answer(
            f"{PE_CHECK} <b>Bekor qilindi</b>",
            reply_markup=get_admin_menu_kb(),
            parse_mode="HTML",
        )
        await _show_admin_panel(message)
        return

    if not message.forward_from_chat:
        text = (
            f"{PE_CROSS} <b>Noto'g'ri format</b>\n\n"
            f"{PE_INFO} Iltimos, kanaldagi xabarni forward qiling."
        )
        await message.answer(text, parse_mode="HTML")
        return

    chat = message.forward_from_chat
    channel_id = chat.id
    channel_username = chat.username
    channel_title = chat.title

    if not channel_username:
        text = (
            f"{PE_CROSS} <b>Kanal username'siz</b>\n\n"
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
                f"{PE_CROSS} <b>Bot kanalda admin emas</b>\n\n"
                f"{PE_INFO} Avval botni kanalga admin qilib qo'shing."
            )
            await message.answer(text, parse_mode="HTML")
            return
    except Exception:
        text = (
            f"{PE_WARNING} <b>Kanalni tekshirib bo'lmadi</b>\n\n"
            f"{PE_INFO} Bot kanalda admin ekanligiga ishonch hosil qiling."
        )
        await message.answer(text, parse_mode="HTML")
        return

    success = await db.add_channel(channel_id, channel_username, channel_title)
    await state.clear()

    if success:
        text = (
            f"{PE_CHECK} <b>Kanal qo'shildi!</b>\n"
            f"{'━' * 28}\n\n"
            f"{PE_CHANNEL} {channel_title}\n"
            f"{PE_GLOBE} @{channel_username}"
        )
    else:
        text = f"{PE_CROSS} <b>Kanal qo'shishda xatolik yuz berdi</b>"

    await message.answer(
        text, reply_markup=get_admin_menu_kb(), parse_mode="HTML"
    )
    await _show_admin_panel(message)


@router.callback_query(F.data.startswith("remove_channel:"))
async def cb_remove_channel(
    callback: CallbackQuery, db: Database
) -> None:
    if not _is_admin(callback.from_user.id):
        return

    channel_id = int(callback.data.split(":", 1)[1])
    success = await db.remove_channel(channel_id)

    if success:
        await callback.answer("Kanal o'chirildi!", show_alert=True)
    else:
        await callback.answer("Xatolik yuz berdi", show_alert=True)

    # Kanallar ro'yxatini yangilash
    channels = await db.get_channels()
    text = (
        f"{PE_CHANNEL} <b>Kanallar boshqaruvi</b>\n"
        f"{'━' * 28}\n\n"
    )
    if channels:
        text += f"{PE_INFO} Majburiy obuna kanallari: <b>{len(channels)}</b> ta"
    else:
        text += f"{PE_INFO} Hozircha hech qanday kanal qo'shilmagan."

    await callback.message.edit_text(
        text,
        reply_markup=get_channel_management_kb(channels),
        parse_mode="HTML",
    )
