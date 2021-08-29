from telebot.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from src.data import Data, User

from src.sections.user import UserSection

from src.staff.updates import Updater

from src.objects import quiz

import configparser
from telebot import TeleBot, logger

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

user_section = UserSection(data=data)

updater = Updater()


@bot.message_handler(commands=["start"])
def start_bot(message):
    user = updater.update_user_interaction_time(message)

    try:
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

    if message_text == "Розклад":
        bot.send_photo(user.chat_id, caption="Розклад цьогорічного BTW",
                       photo="https://ibb.co/VTt9GGX",
                       reply_markup=markup)
    elif message_text == "Чат зі спікерами":
        bot.send_message(user.chat_id,
                         text="Долучайся до нашого чату з спікерами: https://t.me/joinchat/fa4V6BaBQB45Zjhi",
                         reply_markup=markup)
    elif message_text == "Інформація про спікерів":
        user_section.send_speakers_info_menu(user)
    elif message_text == "Виникли запитання?":
        bot.send_message(user.chat_id, text="Звернись до нашого головного організатора @kerril", reply_markup=markup)

    if message_text == "Ірина Клейменова":
        bot.send_photo(user.chat_id,
                       photo="https://ibb.co/njF9Vw6",
                       caption="HR-спеціалістка компанії Fairmarkit. Активістка та волонтерка. Ірина розкаже як новенькі входять в IT та дасть поради початківцям. \n""<a href='https://www.facebook.com/iryna.kleimenova'>Facebook</a> | <a href='https://www.linkedin.com/in/iryna-kley-10aaa41a5'>Linkedin</a>")
    elif message_text == "Інна Шинкаренко":
        bot.send_photo(user.chat_id,
                       photo="https://ibb.co/DCKZTfs",
                       caption="Психологиня, яка допомагає людям відчути і побачити себе. Консультантка терапевтичного проєкту “Точка відліку”. На тренінгу Інна розкаже про емоційне вигорання та допоможе його уникнути. \n""<a href='https://www.facebook.com/iryna.kleimenova'>Facebook</a> | <a href='https://www.linkedin.com/in/inna-shynkarenko-4814525/'>Linkedin</a> | <a href='https://www.instagram.com/inkissh/'>Instagram</a>")
    elif message_text == "Орест Дмитрасевич":
        bot.send_photo(user.chat_id,
                       photo="https://ibb.co/tp9NcTR",
                       caption="Program manager в українській IT-компанії ELEKS. Автор найбільшого блогу в Україні про product management ""<a href='https://t.me/themanagerblog'>Kaizen</a>"".Орест розкаже як починав свій кар’єрний шлях project-менеджера та як досягти успіху в цій сфері. \n""<a href='https://www.facebook.com/o.dmytrasevych'>Facebook</a> | <a href='https://www.linkedin.com/in/odmytrasevych'>Linkedin</a>")
    elif message_text == "Михайло Дубчак":
        bot.send_photo(user.chat_id,
                       photo="https://ibb.co/SKXsyyc",
                       caption="Таргетолог-стратег. Запускає рекламу, яка дійсно приносить прибуток. Знімає цікаві відеоуроки по SMM і таргету на ""<a href='https://www.youtube.com/channel/UCYXrY_QWuVGwQn5sAhhNwnw'>Youtube</a>"". Співзасновник агентства ADC Wind. Михайло розкаже про професію таргетолога та про роль таргетованої реклами в онлайн-маркетингу. \n""<a href='https://www.instagram.com/meta_marketer/'>Instagram</a>")
    elif message_text == "Роксолана Салашник":
        bot.send_photo(user.chat_id,
                       photo="https://ibb.co/yy9QqyG",
                       caption="Спеціалістка з області SMM та маркетингу. Visual content-maker, яка навчить тебе як мислити красиво. Веде інформативний блог в Instagram.Розповість, чому особистий бренд - це нафта 2021 року. \n""<a href='https://www.instagram.com/romeka.stabl/'>Instagram</a>")
    elif message_text == "Софія Телішевська":
        bot.send_photo(user.chat_id,
                       photo="https://ibb.co/dcZd42k",
                       caption="Політична журналістка. Авторка власної telegram-групи ""<a href='https://t.me/mediahospital'>Медіашпиталь</a>"". Софія доступно розкаже як простими словами розповідати про складні речі. \n""<a href='https://www.instagram.com/sonya_telishevska/'>Instagram</a>")
    elif message_text == "Христина Мокрій":
        bot.send_photo(user.chat_id,
                       photo="AgACAgIAAxkBAAIBemEcmIIW2mJ7-oRmGBQmiIus65HNAAJ6tjEbp3DpSBfc5Q4tmfS7AQADAgADeAADIAQ",
                       caption="Громадська діячка. Тренерка soft skills. Організаторка та декораторка подій. Фасилітаторка програми ""Активні громадяни"" від Британської ради. Менеджерка залучення ресурсів у Львівському обласному молодіжному центрі; Засновниця/голова у ГО ""Львівська майстерня організації подій"".\n""<a href='https://www.facebook.com/profile.php?id=100002246408610'>Facebook</a> | <a href='https://www.linkedin.com/in/%D1%85%D1%80%D0%B8%D1%81%D1%82%D0%B8%D0%BD%D0%B0-%D0%BC%D0%BE%D0%BA%D1%80%D1%96%D0%B9-211186119'>Linkedin</a>|<a href='https://instagram.com/k.mokrii?utm_medium=copy_link'>Instagram</a>")
    elif message_text == "Назар Подольчак":
        bot.send_photo(user.chat_id,
                       photo="https://ibb.co/Y2Tz7PG",
                       caption="Професор та доктор економічних наук. Засновник спеціалізованої школи Tech StartUp School. Завідувач кафедри адміністративного та фінансового менеджменту у Львівській політехніці. \n""<a href='https://www.facebook.com/nazarpodolchak'>Facebook</a>|<a href='https://www.linkedin.com/in/nazar-podolchak-36b30b47/'>Linkedin</a> | <a href='https://www.instagram.com/nazarpodolchak/'>Instagram</a>")
    elif message_text == "Марго Васильєва":
        bot.send_photo(user.chat_id,
                       photo="https://ibb.co/0VGtbqB",
                       caption="Дівчина-мандрівниця, яка подолала понад 41 000 км. Одна із засновниць спільноти ""<a href='https://t.me/zlit_dzrhch'>Бакотиків</a>"" - групи різних мандрівників та автостоперів, які подорожують Україною та діляться власними враженнями.Марго розкаже як подорожувати автостопом та дасть поради. \n""<a href='https://instagram.com/margo.v66?utm_medium=copy_link'>Instagram</a>")
    elif message_text == "Назад":
        user_section.send_start_menu(user)


@bot.message_handler(content_types=['photo'])
def photo_id(message):
    if message.chat.username == "naz_furdychka":
        photo_id = message.photo[-1].file_id
        global photo
        photo = photo_id
        bot.send_message(message.chat.id, 'ID of your photo is ' + photo_id)


def send_welcome_message_and_start_quiz(user: User):
    bot.send_photo(
        user.chat_id,
        caption=(
        " Привіт, любий друже!\n"
        "Насувається десятий BEST training week, тиждень мега крутих тренінгів та шерінгів🔥 Тому саме для тебе ми підготували щось дійсно захопливе.Наші спікери розкажуть тобі багато крутої інфи й поділяться власним досвідом✨\n"
        "Пройди реєстрацію і дізнайся, що на тебе чекає📝\n"

    ),
        # photo="https://ibb.co/BLZNq1q",
        photo="https://ibb.co/2KpPHrb"
    )

    final_func = user_section.send_start_menu
    quiz.start_starting_quiz(user, bot, final_func)


if __name__ == "__main__":
    bot.polling(none_stop=True)
