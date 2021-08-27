from telebot.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from .section import Section
from ..data import Data, User


class UserSection(Section):

    def __init__(self, data: Data):
        super().__init__(data=data)

    def send_start_menu(self, user: User):
        btn_schedule = KeyboardButton(text="Розклад")
        btn_info = KeyboardButton(text="Інформація про спікерів")
        btn_chat_link = KeyboardButton(text="Чат зі спікерами")
        btn_contacts = KeyboardButton(text="Виникли запитання?")

        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn_schedule)
        markup.add(btn_info)
        markup.add(btn_chat_link)
        markup.add(btn_contacts)

        self.bot.send_photo(
            user.chat_id,
            caption="Вибери команду з списку)",
            photo="https://ibb.co/BLZNq1q",
            reply_markup=markup,
        )

    def send_speakers_info_menu(self, user: User):
        btn_sp1 = KeyboardButton(text="Ірина Клейменова", )
        btn_sp2 = KeyboardButton(text="Інна Шинкаренко")
        btn_sp3 = KeyboardButton(text="Орест Дмитрасевич")
        btn_sp4 = KeyboardButton(text="Михайло Дубчак")
        btn_sp5 = KeyboardButton(text="Роксолана Салашник")
        btn_sp6 = KeyboardButton(text="Софія Телішевська")
        btn_sp7 = KeyboardButton(text="Христина Мокрій")
        btn_sp8 = KeyboardButton(text="Назар Подольчак")
        btn_sp9 = KeyboardButton(text="Speaker 9")
        btn_back = KeyboardButton(text="Назад")

        markup = ReplyKeyboardMarkup(resize_keyboard=True)

        markup.row(btn_sp1, btn_sp2, btn_sp3)
        markup.row(btn_sp4, btn_sp5, btn_sp6)
        markup.row(btn_sp7, btn_sp8, btn_sp9)

        markup.add(btn_back)
        self.bot.send_message(user.chat_id, text="Тиць по спікеру щоб дізнатись про нього", reply_markup=markup)
