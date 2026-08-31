# Kino Bot

Professional Telegram kino bot — Aiogram 3.x, SQLite, Premium Emojilar.

## Imkoniyatlar

- Kino kodini yuborish orqali tezkor qidirish
- Nom bo'yicha qidirish
- Mashhur va yangi kinolar ro'yxati
- Admin panel (kino qo'shish/o'chirish, statistika, broadcast)
- Majburiy kanal obuna tekshirish
- Deep-link qo'llab-quvvatlash

## Railway'da deploy qilish

1. GitHub'ga push qiling
2. [Railway.app](https://railway.app) ga kiring
3. **New Project** → **Deploy from GitHub Repo** tanlang
4. Repository'ni ulang
5. **Variables** bo'limiga quyidagilarni qo'shing:
   - `BOT_TOKEN` — BotFather'dan olingan token
   - `ADMIN_IDS` — Admin Telegram ID
   - `DB_PATH` — `database/kino_bot.db`
6. Deploy avtomatik boshlanadi

## Texnologiyalar

- Python 3.12
- Aiogram 3.x
- SQLite (aiosqlite)
- Railway (deploy)
