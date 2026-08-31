import os

def insert_debug():
    with open('handlers/admin.py', 'r', encoding='utf-8') as f:
        text = f.read()

    debug_code = '''
@router.message(Command("debug"))
async def cmd_debug(message: Message, bot: Bot) -> None:
    if not _is_admin(message.from_user.id):
        return
    import os
    import config
    
    data_exists = os.path.exists('/data')
    app_data_exists = os.path.exists('/app/data')
    db_path = str(config.DB_PATH)
    
    app_data_contents = "Not found"
    if app_data_exists:
        try:
            app_data_contents = str(os.listdir('/app/data'))
        except Exception as e:
            app_data_contents = f"Error: {e}"
            
    data_contents = "Not found"
    if data_exists:
        try:
            data_contents = str(os.listdir('/data'))
        except Exception as e:
            data_contents = f"Error: {e}"

    msg = (
        f"🛠 <b>Debug Ma'lumotlari:</b>\\n\\n"
        f"<b>DB_PATH (ayni paytda):</b>\\n<code>{db_path}</code>\\n\\n"
        f"<b>/app/data mavjudmi?</b> {app_data_exists}\\n"
        f"Ichidagilar: {app_data_contents}\\n\\n"
        f"<b>/data mavjudmi?</b> {data_exists}\\n"
        f"Ichidagilar: {data_contents}\\n\\n"
        f"<b>Ishchi papka:</b> {os.getcwd()}"
    )
    await message.answer(msg, parse_mode="HTML")
'''

    text = text.replace('#  BAZANI ZAXIRALASH (BACKUP)', debug_code + '\n#  BAZANI ZAXIRALASH (BACKUP)')
    with open('handlers/admin.py', 'w', encoding='utf-8') as f:
        f.write(text)

insert_debug()
print("Debug command inserted")
