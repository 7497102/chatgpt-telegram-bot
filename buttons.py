from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


from utils import *
from configs import LANGUAGES


def generate_languages():
    markup = InlineKeyboardMarkup(row_width=1)
    btn_ru = InlineKeyboardButton(text="Русский 🇷🇺", callback_data='ru')
    btn_uz = InlineKeyboardButton(text="O`zbek 🇺🇿", callback_data='uz')
    btn_en = InlineKeyboardButton(text='English 🇬🇧', callback_data='en')
    markup.add(btn_ru, btn_uz, btn_en)

    return markup


def generate_register_btn(user_lang):
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    text = KeyboardButton(text=f"""{register_btn[user_lang]}""")
    markup.add(text)

    return markup


def generate_phone_number_btn(user_lang):
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    text = KeyboardButton(text=f"""{send_contact[user_lang]}""", request_contact=True)
    markup.add(text)

    return markup


def generate_agree_disagree():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    yes = KeyboardButton(text="YES✅")
    no = KeyboardButton(text="NO❌")
    markup.add(yes, no)

    return markup


def generate_main_menu_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    chatbot = KeyboardButton(text='AI ChatBot 🤖')
    comment = KeyboardButton(text='Comment ✍')
    translator = KeyboardButton(text="AI Translator🤖🔄")
    markup.add(chatbot, translator, comment)

    return markup


def generate_langs():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = []
    for value in LANGUAGES.values():
        btn = KeyboardButton(text=value)
        buttons.append(btn)

    markup.add(*buttons)
    return markup


def generate_back_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_back = KeyboardButton(text="⬅")
    markup.add(btn_back)
    return markup
