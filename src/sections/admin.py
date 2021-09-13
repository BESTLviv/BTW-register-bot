from telebot.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from telebot import logger

from ..data import Data, User
from .section import Section


class AdminSection(Section):

    ADMIN_MENU_PHOTO = "https://i.ibb.co/2qSxy9F/image.jpg"

    def __init__(self, data: Data):
        super().__init__(data=data)

        self.admin_markup = self._form_admin_menu_markup()

    def process_callback(self, call: CallbackQuery, user: User):
        action = call.data.split(";")[1]

        if action == "AdminMenu":
            self.send_mailing_menu(user, call=call)

        elif action == "MailAll":
            self.mail_all(user)

        elif action == "MailMe":
            self.mail_me_test(user)

        elif action == "MailUnregistered":
            self.mail_unregistered(user)

        else:
            self.answer_in_development(call)

        self.bot.answer_callback_query(call.id)

    def process_text(self, text):
        pass

    def send_mailing_menu(self, user: User, call: CallbackQuery = None):
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

        if call:
            self.send_message(
                call, text, photo=self.ADMIN_MENU_PHOTO, reply_markup=markup
            )
        else:
            self.bot.send_photo(
                user.chat_id,
                caption=text,
                photo=self.ADMIN_MENU_PHOTO,
                reply_markup=markup,
            )

    def mail_all(self, user: User):
        text = (
            "Надішли повідомлення яке потрібно розіслати всім\n\n"
            "Якщо потрібно вставити кнопку-посилання, то в останньому рядку тексту напиши посилання формату <b>https... ->btn_name</b>"
        )

        self.bot.send_message(user.chat_id, text=text)
        self.bot.register_next_step_handler_by_chat_id(
            user.chat_id, self._process_mail_users, auditory="all", user=user
        )

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
        self.send_mailing_menu(user)

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

        # Mail me test
        btn_text = "Перевірити кінцеве повідомлення"
        btn_callback = self.form_admin_callback(action="MailMe", edit=True)
        btn_mail_me_test = InlineKeyboardButton(btn_text, callback_data=btn_callback)
        markup.add(btn_mail_me_test)

        return markup
