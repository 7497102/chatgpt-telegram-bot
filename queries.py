import sqlite3


def insert_user_lang(chat_id: int):
    database = sqlite3.connect('chatgpt.db')
    cursor = database.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO languages(tg_id)
        VALUES(?)
    """, (chat_id,))

    database.commit()
    database.close()


def update_user_lang(chat_id: int, language: str):
    db = sqlite3.connect('chatgpt.db')
    cursor = db.cursor()

    cursor.execute("""
        UPDATE OR IGNORE languages
        SET language = ?
        WHERE tg_id = ?
    """, (language, chat_id))

    db.commit()
    db.close()


def get_user_lang(chat_id: int):
    database = sqlite3.connect('chatgpt.db')
    cursor = database.cursor()

    cursor.execute("""
        SELECT language FROM languages
        WHERE tg_id = ?
    """, (chat_id,))
    user_lang = cursor.fetchone()[0]
    database.close()

    return user_lang


def insert_user(telegram_id, full_name, phone_number, email_address):
    database = sqlite3.connect('chatgpt.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO users(telegram_id, full_name, phone_number, email_address)
    VALUES(?,?,?,?)
    ''', (telegram_id, full_name, phone_number, email_address))
    database.commit()
    database.close()


def get_all_users():
    database = sqlite3.connect('chatgpt.db')
    cursor = database.cursor()
    cursor.execute('''
        SELECT telegram_id FROM users;
    ''')
    users = cursor.fetchall()
    users_tg_id = []

    for user in users:
        users_tg_id.append(user[0])

    database.close()

    return users_tg_id


def get_user_data(telegram_id):
    database = sqlite3.connect('chatgpt.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM users
    WHERE telegram_id = ?
    ''', (telegram_id,))

    user_data = cursor.fetchone()
    database.close()
    return user_data