import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")

ADMIN_IDS: list[int] = [
    int(x.strip())
    for x in os.getenv("ADMIN_IDS", "").split(",")
    if x.strip().isdigit()
]


# Agar Railway Volume (/app/data) mavjud bo'lsa, to'g'ridan-to'g'ri o'sha yerdan foydalanamiz
if os.path.exists('/app/data'):
    DB_PATH = Path('/app/data/kino_bot.db')
else:
    DB_PATH = BASE_DIR / os.getenv('DB_PATH', 'database/kino_bot.db')
