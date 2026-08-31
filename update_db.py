import os

def update_db():
    with open('database/db.py', 'r', encoding='utf-8') as f:
        text = f.read()

    old_migration = '''        # Migration for invite_link
        try:
            await self.db.execute("ALTER TABLE channels ADD COLUMN invite_link TEXT")
        except Exception:
            pass
            
        await self.db.commit()'''
        
    new_migration = '''        # Migration for invite_link
        try:
            await self.db.execute("ALTER TABLE channels ADD COLUMN invite_link TEXT")
        except Exception:
            pass
            
        await self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS join_requests (
                user_id INTEGER,
                channel_id INTEGER,
                requested_at TEXT DEFAULT (datetime('now')),
                PRIMARY KEY (user_id, channel_id)
            )
            """
        )
        await self.db.commit()'''

    if old_migration in text:
        text = text.replace(old_migration, new_migration)
        
    old_methods = '''    async def get_channels(self) -> list[aiosqlite.Row]:
        async with self.db.execute("SELECT * FROM channels") as cursor:
            return await cursor.fetchall()'''
            
    new_methods = '''    async def get_channels(self) -> list[aiosqlite.Row]:
        async with self.db.execute("SELECT * FROM channels") as cursor:
            return await cursor.fetchall()

    async def add_join_request(self, user_id: int, channel_id: int) -> None:
        await self.db.execute(
            "INSERT OR IGNORE INTO join_requests (user_id, channel_id) VALUES (?, ?)",
            (user_id, channel_id)
        )
        await self.db.commit()

    async def has_join_request(self, user_id: int, channel_id: int) -> bool:
        async with self.db.execute(
            "SELECT 1 FROM join_requests WHERE user_id = ? AND channel_id = ?",
            (user_id, channel_id)
        ) as cursor:
            row = await cursor.fetchone()
            return row is not None'''

    if old_methods in text:
        text = text.replace(old_methods, new_methods)

    with open('database/db.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Database updated!")

update_db()
