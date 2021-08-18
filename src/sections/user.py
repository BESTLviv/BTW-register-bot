from telebot.types import (
    CallbackQuery,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from ..data import Data, User
from ..objects import quiz
from .section import Section
from ..staff import utils
from random import randint


class UserSection(Section):
    TEXT_BUTTONS = ["Найти вакансію", "Хто ми?", "Профіль"]

    def __init__(self, data: Data):
        super().__init__(data=data)

    def process_callback(self, call: CallbackQuery, user: User):
        action = call.data.split(";")[1]

        # check if user is not HR
        if user.hr_status is True:
            self.bot.answer_callback_query(call.id, text="HR не має доступу сюди :(")
            return

        if action == "ApplyVacancy":
            vacancy_id = call.data.split(";")[3]
            self.apply_for_vacancy(user, vacancy_id, call=call)

        elif action == "VacInfo":
            self.send_vacancy_info(user, call=call)

        elif action == "Profile":
            self.send_profile_menu(user, call)

        elif action == "Interests":
            self.send_filters_menu(call, user, interest=True)

        elif action == "Experience":
            self.send_filters_menu(call, user, experience=True)

        elif action == "Employment":
            self.send_filters_menu(call, user, employment=True)

        elif action == "CV":
            self.send_cv_request(call, user)

        else:
            self.answer_wrong_action(call)

        self.bot.answer_callback_query(call.id)

    def process_text(self, text: str, user: User):

        # check if user is not HR
        if user.hr_status is True:
            self.bot.send_message(user.chat_id, text="HR не має доступу сюди :(")
            return

        if text == self.TEXT_BUTTONS[0]:
            self.send_vacancy_info(user, is_random=True)

        elif text == self.TEXT_BUTTONS[1]:
            self.send_about_info(user)

        elif text == self.TEXT_BUTTONS[2]:
            self.send_profile_menu(user)

    def send_start_menu(self, user: User):
        ejf = self.data.get_btw()

        btn_schedule = KeyboardButton(text="Розклад")
        btn_info = KeyboardButton(text="Інформація про спікерів")
        btn_chat_link = KeyboardButton(text="Чат зі спікерами")
        btn_contacts = KeyboardButton(text="Виникли запитання?")

        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn_schedule)
        markup.add(btn_info)
        markup.add(btn_chat_link)
        markup.add(btn_contacts)

        # MOCK

        # self.bot.send_photo(
        #     user.chat_id,
        #     caption=ejf.content.user_start_text,
        #     photo=ejf.content.user_start_photo,
        #     reply_markup=markup,
        # )

        self.bot.send_photo(
            user.chat_id,
            caption="Вибери команду з списку)",
            photo="AgACAgIAAxkBAAIBamEcllsyg1TiygG-0SHs_Pzg3Qk4AAJ3tjEbp3DpSDnC36SJ31ADAQADAgADeAADIAQ",
            reply_markup=markup,
        )

    def send_profile_menu(self, user: User, call: CallbackQuery = None):
        text_message = """
        """
        text_message += self._form_profile_vacancy_count_text(user)

        markup = self._form_profile_menu_markup()

        if call is None:
            self.bot.send_message(
                chat_id=user.chat_id, text=text_message, reply_markup=markup
            )
        else:
            self.send_message(call, text=text_message, reply_markup=markup)

    def send_speakers_info_menu(self, user: User):
        btn_sp1 = KeyboardButton(text="Speaker 1",)
        btn_sp2 = KeyboardButton(text="Speaker 2")
        btn_sp3 = KeyboardButton(text="Speaker 3")
        btn_sp4 = KeyboardButton(text="Speaker 4")
        btn_sp5 = KeyboardButton(text="Speaker 5")
        btn_sp6 = KeyboardButton(text="Speaker 6")
        btn_sp7 = KeyboardButton(text="Speaker 7")
        btn_sp8 = KeyboardButton(text="Speaker 8")
        btn_sp9 = KeyboardButton(text="Speaker 9")
        btn_back = KeyboardButton(text="Назад")

        markup = ReplyKeyboardMarkup(resize_keyboard=True)

        markup.row(btn_sp1,btn_sp2,btn_sp3)
        markup.row(btn_sp4,btn_sp5,btn_sp6)
        markup.row(btn_sp7,btn_sp8,btn_sp9)

        markup.add(btn_back)
        self.bot.send_message(user.chat_id,text="Тиць по спікеру щоб дізнатись про нього", reply_markup=markup)

    def send_about_info(self, user: User):
        self.bot.send_message(user.chat_id, text="Test")
