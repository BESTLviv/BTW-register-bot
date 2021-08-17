from telebot.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from telebot import logger

from ..data import Data, User, BTW
from .section import Section
from ..staff import utils


class AdminSection(Section):

    ADMIN_MENU_PHOTO = "https://i.ibb.co/2qSxy9F/image.jpg"

    def __init__(self, data: Data):
        super().__init__(data=data)

        self.admin_markup = self._form_admin_menu_markup()

    def process_callback(self, call: CallbackQuery, user: User):
        action = call.data.split(";")[1]

        if action == "AdminMenu":
            self.send_admin_menu(user, call=call)

        elif action == "SendMessageMenu":
            self.send_mailing_menu(call, user)

        elif action == "MailAll":
            self.mail_all(user)

        elif action == "MailMe":
            self.mail_me_test(user)

        elif action == "MailUnregistered":
            self.mail_unregistered(user)

        elif action == "MailNonCV":
            self.mail_non_cv(user)

        elif action == "Statistic":
            self.send_statistic(call, user)

        else:
            self.answer_in_development(call)

        self.bot.answer_callback_query(call.id)

    def process_text(self, text):
        pass

    def send_admin_menu(self, user: User, call: CallbackQuery = None):
        text = "Ну прівєт Адміністратор цього бота!"

        if call is None:
            self.bot.send_photo(
                chat_id=user.chat_id,
                caption=text,
                photo=self.ADMIN_MENU_PHOTO,
                reply_markup=self.admin_markup,
            )
        else:
            self.send_message(
                call,
                text=text,
                photo=self.ADMIN_MENU_PHOTO,
                reply_markup=self.admin_markup,
            )

    def send_statistic(self, call: CallbackQuery, user: User):
        self.answer_in_development(call)


    def mail_all(self, user: User):
        text = (
            "Надішли повідомлення яке потрібно розіслати всім\n\n"
            "Якщо потрібно вставити кнопку-посилання, то в останньому рядку тексту напиши посилання формату <b>https... ->btn_name</b>"
        )

        self.bot.send_message(user.chat_id, text=text)
        self.bot.register_next_step_handler_by_chat_id(
            user.chat_id, self._process_mail_users, auditory="all", user=user
        )

    def send_mailing_menu(self, call: CallbackQuery, user: User):
        chat_id = user.chat_id

        # form text
        user_count = User.objects.count()
        user_registered_count = User.objects.filter(additional_info__ne=None).count()
        user_not_blocked_count = User.objects.filter(is_blocked=False).count()
        text = (
            f"Всього стартануло бот - <b>{user_count}</b>\n"
            f"Пройшло реєстрацію - <b>{user_registered_count}</b>\n"
            f"Всього не заблокованих користувачів - <b>{user_not_blocked_count}</b>"
        )

        markup = self._form_mailing_markup()

        self.send_message(call, text, photo=self.ADMIN_MENU_PHOTO, reply_markup=markup)

    def mail_me_test(self, user: User):
        text = (
            "Надішли повідомлення для тесту і я надішлю тобі його кінцевий вигляд\n\n"
            "Якщо потрібно вставити кнопку-посилання, то в останньому рядку тексту напиши посилання формату <b>https... ->btn_name</b>"
        )

        self.bot.send_message(user.chat_id, text=text)
        self.bot.register_next_step_handler_by_chat_id(
            user.chat_id, self._process_mail_users, auditory="me", user=user
        )

    def mail_unregistered(self, user: User):
        text = (
            "Надішли повідомлення і я надішлю його всім учасникам які ще не пройшли опитування\n\n"
            "Якщо потрібно вставити кнопку-посилання, то в останньому рядку тексту напиши посилання формату <b>https... ->btn_name</b>"
        )

        self.bot.send_message(user.chat_id, text=text)
        self.bot.register_next_step_handler_by_chat_id(
            user.chat_id, self._process_mail_users, auditory="unregistered", user=user
        )

    def mail_non_cv(self, user: User):
        text = (
            "Надішли повідомлення і я надішлю його всім учасникам які не загрузили свої CV\n\n"
            "Якщо потрібно вставити кнопку-посилання, то в останньому рядку тексту напиши посилання формату <b>https... ->btn_name</b>"
        )

        self.bot.send_message(user.chat_id, text=text)
        self.bot.register_next_step_handler_by_chat_id(
            user.chat_id, self._process_mail_users, auditory="no_cv", user=user
        )

    def send_message_to_auditory(
        self,
        admin_chat_id,
        text: str,
        photo: str,
        markup: InlineKeyboardMarkup,
        user: User,
        auditory="all",
    ):
        def send_message(receiver: User, text=None, photo=None, markup=None):
            try:
                if photo:
                    self.bot.send_photo(
                        receiver.chat_id, caption=text, photo=photo, reply_markup=markup
                    )
                else:
                    self.bot.send_message(receiver.chat_id, text, reply_markup=markup)
                return True
            except Exception as e:
                err_text = f"User @{receiver.username} {receiver.chat_id} didn't receive message - {e}"
                logger.error(err_text)
                self.bot.send_message(chat_id=admin_chat_id, text=err_text)
                receiver.is_blocked = True
                receiver.save()

        if auditory == "all":
            users = User.objects.filter(additional_info__ne=None)

        elif auditory == "me":
            users = [user]

        elif auditory == "unregistered":
            users = User.objects.filter(additional_info=None)

        elif auditory == "no_cv":
            users = User.objects.filter(cv_file_id=None, additional_info__ne=None)

        else:
            self.bot.send_message(
                chat_id=admin_chat_id, text="шось не так, не та аудиторія"
            )

        # sending messages
        counter = 0

        for receiver in users:
            if send_message(receiver, text, photo, markup):
                counter += 1

        success_text = f"Повідомлення відправлено {counter} користувачам"
        self.bot.send_message(chat_id=admin_chat_id, text=success_text)

        # send start markup
        self.send_admin_menu(user)

    def _process_mail_users(self, message, **kwargs):
        """
        :param auditory: "all" to mail all, else set it to one of auditory type from ejf_table
        :param user: user object from db
        """
        auditory = kwargs["auditory"]
        user = kwargs["user"]

        text = str()
        photo = str()
        url = str()
        markup = InlineKeyboardMarkup()

        if message.content_type == "text":
            text = message.text

        elif message.content_type == "photo":
            text = message.caption
            photo = message.photo[-1].file_id

        else:
            self.mail_all(user)
            return

        # find if there is link in text and form markup
        try:
            if text:
                text_splitted = text.split("\n")
                last_row = text_splitted[-1]
                if "https" in last_row and "->" in last_row:
                    text = "\n".join(text_splitted[:-1])

                    # form button
                    url, btn_text = last_row.split("->")
                    btn = InlineKeyboardButton(text=btn_text, url=url)
                    markup.add(btn)
        except Exception as e:
            print(f"{e} during mailing")
            self.bot.send_message(
                message.chat.id, text=f"Щось пішло не так з посиланням - {e}"
            )

        self.send_message_to_auditory(
            admin_chat_id=message.chat.id,
            text=text,
            photo=photo,
            markup=markup,
            user=user,
            auditory=auditory,
        )

    def _form_admin_menu_markup(self) -> InlineKeyboardMarkup:

        admin_markup = InlineKeyboardMarkup()

        # company button
        btn_text = "Компанії"
        btn_callback = self.form_admin_callback(action="CompanyList", edit=True)
        company_btn = InlineKeyboardButton(text=btn_text, callback_data=btn_callback)
        admin_markup.add(company_btn)

        # mailing button
        btn_text = "Розсилка"
        btn_callback = self.form_admin_callback(action="SendMessageMenu", edit=True)
        mailing_btn = InlineKeyboardButton(text=btn_text, callback_data=btn_callback)
        admin_markup.add(mailing_btn)

        # statistic button
        btn_text = "Статистика"
        btn_callback = self.form_admin_callback(action="Statistic", edit=True)
        statistic_btn = InlineKeyboardButton(text=btn_text, callback_data=btn_callback)
        admin_markup.add(statistic_btn)

        # cv button
        btn_text = "CV"
        btn_callback = self.form_admin_callback(action="CVMenu", edit=True)
        cv_btn = InlineKeyboardButton(text=btn_text, callback_data=btn_callback)
        admin_markup.add(cv_btn)

        return admin_markup


    def _form_cv_menu_markup(self) -> InlineKeyboardMarkup:
        cv_menu_markup = InlineKeyboardMarkup()

        # download last archive
        btn_text = "Завантажити останній архів CV"
        btn_callback = self.form_admin_callback(action="CVDownloadLast", edit=True)
        cv_last_btn = InlineKeyboardButton(text=btn_text, callback_data=btn_callback)
        cv_menu_markup.add(cv_last_btn)

        # create & download new archive
        btn_text = "Завантажити оновлений архів"
        btn_callback = self.form_admin_callback(action="CVDownloadNew", edit=True)
        cv_new_btn = InlineKeyboardButton(text=btn_text, callback_data=btn_callback)
        cv_menu_markup.add(cv_new_btn)

        # back button
        btn_callback = self.form_admin_callback(action="AdminMenu", edit=True)
        back_btn = self.create_back_button(callback_data=btn_callback)
        cv_menu_markup.add(back_btn)

        return cv_menu_markup


    def _form_company_menu_markup(self, company_id) -> InlineKeyboardMarkup:

        company_menu_markup = InlineKeyboardMarkup()

        # company vacancies button
        btn_text = "Список вакансій"
        btn_callback = self.form_admin_callback(
            action="VacancyList", company_id=company_id, edit=True
        )
        vacancy_list_btn = InlineKeyboardButton(
            text=btn_text, callback_data=btn_callback
        )
        company_menu_markup.add(vacancy_list_btn)

        # company key button
        btn_text = "Отримати ключ"
        btn_callback = self.form_admin_callback(
            action="CompanyKey", company_id=company_id, edit=True
        )
        company_key_btn = InlineKeyboardButton(
            text=btn_text, callback_data=btn_callback
        )
        company_menu_markup.add(company_key_btn)

        btn_callback = self.form_admin_callback(action="CompanyList", edit=True)
        btn_back = self.create_back_button(btn_callback)
        company_menu_markup.add(btn_back)

        return company_menu_markup


    def _form_mailing_markup(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        # Mail all auditory
        btn_text = "Розсилка на всю аудиторію"
        btn_callback = self.form_admin_callback(action="MailAll", edit=True)
        btn_mail_all = InlineKeyboardButton(btn_text, callback_data=btn_callback)
        markup.add(btn_mail_all)

        # Mail unregistered auditory
        btn_text = "Розсилка на незареєстрованих"
        btn_callback = self.form_admin_callback(action="MailUnregistered", edit=True)
        btn_mail_unregistered = InlineKeyboardButton(
            btn_text, callback_data=btn_callback
        )
        markup.add(btn_mail_unregistered)

        # Mail non cv auditory
        btn_text = "Розсилка на безсівішних"
        btn_callback = self.form_admin_callback(action="MailNonCV", edit=True)
        btn_mail_non_cv = InlineKeyboardButton(btn_text, callback_data=btn_callback)
        markup.add(btn_mail_non_cv)

        # Mail me test
        btn_text = "Перевірити кінцеве повідомлення"
        btn_callback = self.form_admin_callback(action="MailMe", edit=True)
        btn_mail_me_test = InlineKeyboardButton(btn_text, callback_data=btn_callback)
        markup.add(btn_mail_me_test)

        # Back button
        btn_callback = self.form_admin_callback(action="AdminMenu", edit=True)
        back_btn = self.create_back_button(btn_callback)
        markup.add(back_btn)

        return markup
