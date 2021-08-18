from telebot.types import (
    CallbackQuery,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from src.data import Data, User

from src.sections.admin import AdminSection
from src.sections.job_fair import BTWSection
from src.sections.user import UserSection


from src.staff.updates import Updater
from src.staff import utils

from src.objects import quiz

import configparser
from telebot import TeleBot, logger

import test_bot

import logging, os

logger.setLevel(logging.INFO)

logger.info("Initializing settings")

config = configparser.ConfigParser()
config.read("Settings.ini")

logger.info("Settings read")

API_TOKEN = (
    os.environ.get("TOKEN", False)
    if os.environ.get("TOKEN", False)
    else config["TG"]["token"]
)
CONNECTION_STRING = (
    os.environ.get("DB", False)
    if os.environ.get("DB", False)
    else config["Mongo"]["db"]
)

bot = TeleBot(API_TOKEN, parse_mode="HTML")
data = Data(conn_string=CONNECTION_STRING, bot=bot)

logger.info("Connected to db")

admin_section = AdminSection(data=data)
job_fair_section = BTWSection(data=data)
user_section = UserSection(data=data)

updater = Updater()


@bot.message_handler(commands=["start"])
def start_bot(message):
    user = updater.update_user_interaction_time(message)

    try:
        # If it is the first start
        if user.additional_info is None:
            send_welcome_message_and_start_quiz(user)

        else:
            user_section.send_start_menu(user=user)

    except Exception as e:
        print(f"Exception during start - {e}")


@bot.message_handler(content_types=["text"])
def handle_text_buttons(message):
    message_text = message.text
    user = updater.update_user_interaction_time(message)
    btn_schedule = KeyboardButton(text="Розклад")
    btn_info = KeyboardButton(text="Інформація про спікерів")
    btn_chat_link = KeyboardButton(text="Чат зі спікерами")
    btn_contacts = KeyboardButton(text="Виникли запитання?")

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(btn_schedule)
    markup.add(btn_info)
    markup.add(btn_chat_link)
    markup.add(btn_contacts)

    if message_text=="Розклад":
        bot.send_photo(user.chat_id, caption="Розклад цьогорічного BTW",photo="AgACAgIAAxkBAAIBcGEclsI-CSlvekp9zsphoXR7GwABggACebYxG6dw6UiZehC1A38tBQEAAwIAA3gAAyAE",reply_markup=markup)
    elif message_text=="Чат зі спікерами":
        bot.send_message(user.chat_id, text="Долучайся до нашого чату з спікерами: https://t.me/joinchat/fa4V6BaBQB45Zjhi", reply_markup=markup)
    elif message_text=="Інформація про спікерів":
        user_section.send_speakers_info_menu(user)
    elif message_text=="Виникли запитання?":
        bot.send_message(user.chat_id, text="Звернись до нашого головного організатора @kerril", reply_markup=markup)

    if message_text == "Speaker 1":
        bot.send_photo(user.chat_id,
                       photo="AgACAgIAAxkBAAIBemEcmIIW2mJ7-oRmGBQmiIus65HNAAJ6tjEbp3DpSBfc5Q4tmfS7AQADAgADeAADIAQ",
                       caption="Info speaker 1")
    elif message_text == "Speaker 2":
        bot.send_photo(user.chat_id,
                       photo="AgACAgIAAxkBAAIBemEcmIIW2mJ7-oRmGBQmiIus65HNAAJ6tjEbp3DpSBfc5Q4tmfS7AQADAgADeAADIAQ",
                       caption="Info speaker 2")
    elif message_text == "Speaker 3":
        bot.send_photo(user.chat_id,
                       photo="AgACAgIAAxkBAAIBemEcmIIW2mJ7-oRmGBQmiIus65HNAAJ6tjEbp3DpSBfc5Q4tmfS7AQADAgADeAADIAQ",
                       caption="Info speaker 3")
    elif message_text == "Speaker 4":
        bot.send_photo(user.chat_id,
                       photo="AgACAgIAAxkBAAIBemEcmIIW2mJ7-oRmGBQmiIus65HNAAJ6tjEbp3DpSBfc5Q4tmfS7AQADAgADeAADIAQ",
                       caption="Info speaker 4")
    elif message_text == "Speaker 5":
        bot.send_photo(user.chat_id,
                       photo="AgACAgIAAxkBAAIBemEcmIIW2mJ7-oRmGBQmiIus65HNAAJ6tjEbp3DpSBfc5Q4tmfS7AQADAgADeAADIAQ",
                       caption="Info speaker 5")
    elif message_text == "Speaker 6":
        bot.send_photo(user.chat_id,
                       photo="AgACAgIAAxkBAAIBemEcmIIW2mJ7-oRmGBQmiIus65HNAAJ6tjEbp3DpSBfc5Q4tmfS7AQADAgADeAADIAQ",
                       caption="Info speaker 6")
    elif message_text == "Speaker 7":
        bot.send_photo(user.chat_id,
                       photo="AgACAgIAAxkBAAIBemEcmIIW2mJ7-oRmGBQmiIus65HNAAJ6tjEbp3DpSBfc5Q4tmfS7AQADAgADeAADIAQ",
                       caption="Info speaker 7")
    elif message_text == "Speaker 8":
        bot.send_photo(user.chat_id,
                       photo="AgACAgIAAxkBAAIBemEcmIIW2mJ7-oRmGBQmiIus65HNAAJ6tjEbp3DpSBfc5Q4tmfS7AQADAgADeAADIAQ",
                       caption="Info speaker 8")
    elif message_text == "Speaker 9":
        bot.send_photo(user.chat_id,
                       photo="AgACAgIAAxkBAAIBemEcmIIW2mJ7-oRmGBQmiIus65HNAAJ6tjEbp3DpSBfc5Q4tmfS7AQADAgADeAADIAQ",
                       caption="Info speaker 9")
    elif message_text == "Назад":
        user_section.send_start_menu(user)

@bot.message_handler(content_types=['photo'])
def photo_id(message):
    if message.chat.username=="naz_furdychka":
        photo_id = message.photo[-1].file_id
        global photo
        photo = photo_id
        bot.send_message(message.chat.id, 'ID of your photo is ' + photo_id)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    user = updater.update_user_interaction_time(call.message)
    bot.clear_step_handler_by_chat_id(user.chat_id)
    section = call.data.split(";")[0]

    try:
        if section == "Admin":
            admin_section.process_callback(call=call, user=user)

        elif section == "DELETE":
            utils.delete_message(bot=bot, call=call)

        elif section == "IGNORE":
            bot.answer_callback_query(call.id)

    except Exception as e:
        print(f"Exception during {section}.{call.data.split(';')[1]} btn tap - {e}")


# @bot.message_handler(content_types=["text"])
# def handle_text_buttons(message):
#     user = updater.update_user_interaction_time(message)
#     message_text = message.text
#     print("here")
#     try:
#
#         JobFair buttons
        # if message_text in job_fair_section.TEXT_BUTTONS:
        #     job_fair_section.process_text(message_text, user)
        #
        # Call admin menu
        # elif message_text == data.ADMIN_PASSWORD:
        #     admin_section.send_admin_menu(user=user)
        #
        # Trigger special commands
        # elif message_text.startswith("ejf__"):
        #     test_bot.process_tests_text(
        #         bot, user, data, message_text, user_section.send_start_menu
        #     )
        #
        # else:
        #     pass  # TODO: answer user that it was invalid input (in utils.py maybe)
    #
    # except Exception as e:
    #     print(e)


def send_welcome_message_and_start_quiz(user: User):
    ejf = data.get_btw()
    # MOCK
    welcome_text = ejf.content.start_text
    # welcome_photo = ejf.content.start_photo

    # bot.send_photo(user.chat_id, photo=welcome_photo, caption=welcome_text)

    # welcome_text = "hello"
    bot.send_message(user.chat_id, text=welcome_text)

    final_func = user_section.send_start_menu
    quiz.start_starting_quiz(user, bot, final_func)


if __name__ == "__main__":
    bot.polling(none_stop=True)
