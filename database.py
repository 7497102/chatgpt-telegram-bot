import sqlite3


database = sqlite3.connect('chatgpt.db')
cursor = database.cursor()


def create_lang_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS languages(
            language_id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id INTEGER UNIQUE,
            language TEXT DEFAULT ""
        )
    """)


create_lang_table()


def create_users_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id BIGINT UNIQUE,
        full_name TEXT,
        email_address TEXT,
        phone_number TEXT
    )
    ''')


create_users_table()