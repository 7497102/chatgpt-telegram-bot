from telebot import TeleBot
from telebot.types import Message, \
    ReplyKeyboardRemove, \
    CallbackQuery
import openai
from googletrans import Translator

from configs import *
from queries import *
from buttons import *
from utils import *

bot = TeleBot(token=TOKEN, parse_mode='HTML')
openai.api_key = "Your openai API KEY"

users_data = {}


@bot.message_handler(commands=['start'])
def start(message: Message):
    chat_id = message.chat.id
    users = get_all_users()
    if chat_id in users:
        main_menu(message)
    else:
        insert_user_lang(chat_id)
        bot.send_message(chat_id, f'''<b>Выберите язык: 🇷🇺
    Tilni tanlang: 🇺🇿
    Choose the language: 🇬🇧</b>''', reply_markup=generate_languages())


@bot.callback_query_handler(func=lambda call: call.data in ['ru', 'uz', 'en'])
def add_users_lang(call: CallbackQuery):
    chat_id = call.message.chat.id
    language = call.data
    update_user_lang(chat_id, language)
    bot.delete_message(chat_id, message_id=call.message.message_id)
    greeting(message=call.message)


def greeting(message: Message):
    chat_id = message.chat.id
    user_lang = get_user_lang(chat_id)
    bot.send_message(chat_id, f"""{starting[user_lang]}""", reply_markup=generate_register_btn(user_lang))


@bot.message_handler(func=lambda message: message.text == "Ro'yxatdan o'tish📋✅" or
                                          message.text == "Зарегистрироваться📋✅" or
                                          message.text == "Register📋✅")
def ask_full_name(message: Message):
    global users_data
    chat_id = message.chat.id
    user_lang = get_user_lang(chat_id)
    users_data[chat_id] = {
        "user_id": chat_id
    }
    print(users_data)
    msg = bot.send_message(chat_id, f"""{registration['ask_fullname'][user_lang]}""",
                           reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, ask_email)


def ask_email(message: Message):
    global users_data
    chat_id = message.chat.id
    user_lang = get_user_lang(chat_id)
    full_name = message.text
    users_data[chat_id].update({"full_name": full_name})
    print(users_data)
    msg = bot.send_message(chat_id, f"""{registration['ask_email'][user_lang]}""")
    bot.register_next_step_handler(msg, ask_phone_number)


def ask_phone_number(message: Message):
    global users_data
    chat_id = message.chat.id
    user_lang = get_user_lang(chat_id)
    email = message.text
    users_data[chat_id].update({"email": email})
    print(users_data)
    msg = bot.send_message(chat_id, f"""{registration['ask_phone_number'][user_lang]}""",
                           reply_markup=generate_phone_number_btn(user_lang))
    bot.register_next_step_handler(msg, show_data)


def show_data(message: Message):
    global users_data
    chat_id = message.chat.id
    user_lang = get_user_lang(chat_id)
    if message.content_type == 'contact':
        phone_number = message.contact.phone_number
        users_data[chat_id].update({'contact': phone_number})
        print(users_data)
    elif message.content_type == 'text':
        phone_number = message.text
        users_data[chat_id].update({'contact': phone_number})
        print(users_data)
    if user_lang == 'uz':
        msg = bot.send_message(chat_id, f"""Ism va familya: <i>{users_data[chat_id]['full_name']}</i>
Telefon raqam: <b>{users_data[chat_id]['contact']}</b>""", reply_markup=generate_agree_disagree())
        bot.register_next_step_handler(msg, agree_disagree)
    elif user_lang == 'ru':
        msg = bot.send_message(chat_id, f"""Имя и фамилия: <i>{users_data[chat_id]['full_name']}</i>
Номер телефона: <b>{users_data[chat_id]['contact']}</b>""", reply_markup=generate_agree_disagree())
        bot.register_next_step_handler(msg, agree_disagree)
    elif user_lang == 'en':
        msg = bot.send_message(chat_id, f"""Full name: <i>{users_data[chat_id]['full_name']}</i>
Email address: {users_data[chat_id]['email']}
Phone number: {users_data[chat_id]['contact']}""", reply_markup=generate_agree_disagree())
        bot.register_next_step_handler(msg, agree_disagree)


def agree_disagree(message: Message):
    global users_data
    chat_id = message.chat.id
    if message.text == "YES✅":
        verify_img(message)
    elif message.text == "NO❌":
        users_data.pop(chat_id)
        greeting(message)


def verify_img(message: Message):
    global users_data
    chat_id = message.chat.id
    user_lang = get_user_lang(chat_id)
    print(users_data)
    with open('apples.jpg', 'rb') as photo:
        msg = bot.send_photo(chat_id, photo,
                             caption=f"""{registration['verify_img'][user_lang]}""",
                             reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, verify_account)


def verify_account(message: Message):
    chat_id = message.chat.id
    user_lang = get_user_lang(chat_id)
    if message.text == "3":
        insert_user(telegram_id=chat_id, full_name=users_data[chat_id]['full_name'],
                    email_address=users_data[chat_id]['email'],
                    phone_number=users_data[chat_id]['contact'])
        bot.send_message(chat_id, f"""{verify['verified'][user_lang]}""")
        main_menu(message)
    else:
        bot.send_message(chat_id, f"""{verify['not verified'][user_lang]}""")
        verify_img(message)


def main_menu(message: Message):
    chat_id = message.chat.id
    user_lang = get_user_lang(chat_id)
    bot.send_message(chat_id, f"""{choose[user_lang]}""", reply_markup=generate_main_menu_btn())


@bot.message_handler(func=lambda message: message.text == "AI ChatBot 🤖")
def ask(message: Message):
    chat_id = message.chat.id
    user_lang = get_user_lang(chat_id)
    msg = bot.send_message(chat_id, f"""{ask_user[user_lang]}""")
    bot.register_next_step_handler(msg, handle_message)


@bot.message_handler(func=lambda message: True)
def handle_message(message: Message):
    try:
        if message.text == 'AI Translator🤖🔄':
            ask_first_language(message)
        elif message.text == 'Comment ✍':
            ask_feedback(message)
        else:
            user_input = message.text
            response = generate_response(user_input)
            bot.reply_to(message, response)
    except Exception as e:
        error_message = "Please try again after 1 minute❗" + str(e)
        bot.reply_to(message, error_message)


def generate_response(user_input, max_tokens=1000):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_input,
            max_tokens=max_tokens
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return "Error generating response: " + str(e)


@bot.message_handler(func=lambda message: message.text == "AI Translator🤖🔄")
def ask_first_language(message: Message):
    user_id = message.from_user.id
    mss = bot.send_message(user_id, f"""Please choose from which language do you want to translate:""",
                           reply_markup=generate_langs())
    bot.register_next_step_handler(mss, ask_second_language)


def ask_second_language(message: Message):
    user_id = message.from_user.id
    first_language = message.text
    mss = bot.send_message(user_id, f"""Please choose to which language do you want to translate:""",
                           reply_markup=generate_langs())
    bot.register_next_step_handler(mss, ask_text, first_language)


def ask_text(message: Message, first_language):
    user_id = message.from_user.id
    second_language = message.text
    mss = bot.send_message(user_id, f"""Please, send me text/word you want to translate:""",
                           reply_markup=ReplyKeyboardRemove())

    bot.register_next_step_handler(mss, translate, first_language, second_language)


def translate(message: Message, first_language, second_language):
    user_id = message.from_user.id
    org_text = message.text
    translator = Translator()
    translated_text = translator.translate(src=first_language.split(' ')[0],
                                           dest=second_language.split(' ')[0],
                                           text=org_text).text
    bot.send_message(user_id, translated_text, reply_markup=generate_main_menu_btn())


@bot.message_handler(func=lambda message: message.text == "Fikr bildirish ✍")
def ask_feedback(message: Message):
    chat_id = message.chat.id
    user_lang = get_user_lang(chat_id)
    msg = bot.send_message(chat_id, f"""{comment['ask_comment'][user_lang]}""",
                           reply_markup=generate_back_btn())
    bot.register_next_step_handler(msg, thanks_for_feedback)


def thanks_for_feedback(message: Message):
    chat_id = message.chat.id
    if message.text == '⬅':
        main_menu(message)
    else:
        user_lang = get_user_lang(chat_id)
        feedback = message.text
        user_data = get_user_data(chat_id)
        bot.send_message(FEEDBACK_CHANNEL, f"""Ism, Familya: {user_data[2]}
Telefon raqami: {user_data[4]}
Feedback: {feedback}""")
        bot.send_message(chat_id, f"""{comment['gratitude'][user_lang]}""")
        main_menu(message)


bot.polling(none_stop=True)
