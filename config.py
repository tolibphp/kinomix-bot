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


# Railway Volume yo'llarini avtomatik qidirish
if os.getenv('DB_PATH'):
    DB_PATH = Path(os.getenv('DB_PATH'))
elif os.path.exists('/data'):
    DB_PATH = Path('/data/kino_bot.db')
elif os.path.exists('/app/data'):
    DB_PATH = Path('/app/data/kino_bot.db')
else:
    DB_PATH = BASE_DIR / 'database' / 'kino_bot.db'
