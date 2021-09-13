from telebot.types import InlineKeyboardButton, CallbackQuery, InputMediaPhoto

from ..data import Data, User


class Section:
    def __init__(self, data: Data):
        self.data = data
        self.bot = data.bot

    def process_callback(self, call: CallbackQuery, user: User):
        pass

    def process_text(self, call: CallbackQuery, user: User):
        pass

    def answer_in_development(self, call: CallbackQuery):
        in_development_text = "В розробці"
        self.bot.answer_callback_query(call.id, text=in_development_text)

    def form_admin_callback(
        self,
        action,
        user_id="",
        company_id="",
        vacancy_id="",
        edit=False,
        delete=False,
        new=False,
    ):
        prev_msg_action = self._get_prev_msg_action(edit, delete, new)
        return f"Admin;{action};{user_id};{company_id};{vacancy_id};{prev_msg_action}"

    def send_message(
        self, call: CallbackQuery, text=None, photo=None, reply_markup=None
    ):
        """Send next message doing something with the previous message.\n
        Every callback_data must have parameter (the last one)
        that says what to do with previous message:
            "Delete", "Edit" or "New"
        """
        chat_id = call.message.chat.id
        message_id = call.message.message_id
        prev_msg_action = call.data.split(";")[-1]

        # Do Smth with previous message (if needed)
        if prev_msg_action == "Delete":
            self.bot.delete_message(chat_id, message_id)

        elif prev_msg_action == "Edit":
            try:
                if photo is None:
                    if call.message.text != text:
                        self.bot.edit_message_text(
                            chat_id=chat_id,
                            message_id=message_id,
                            text=text,
                            reply_markup=reply_markup,
                        )
                    else:
                        self.bot.edit_message_reply_markup(
                            chat_id=chat_id,
                            message_id=message_id,
                            reply_markup=reply_markup,
                        )
                # edit caption + photo
                elif photo and call.message.content_type == "photo":
                    # if photo was edited
                    if call.message.photo[0].file_id != photo:
                        self.bot.edit_message_media(
                            chat_id=chat_id,
                            message_id=message_id,
                            media=InputMediaPhoto(
                                photo, caption=text, parse_mode="HTML"
                            ),
                            reply_markup=reply_markup,
                        )
                    # if text was edited
                    elif call.message.caption != text:
                        self.bot.edit_message_caption(
                            chat_id=chat_id,
                            message_id=message_id,
                            caption=text,
                            reply_markup=reply_markup,
                        )
                    # if markup was edited
                    else:
                        self.bot.edit_message_reply_markup(
                            chat_id=chat_id,
                            message_id=message_id,
                            reply_markup=reply_markup,
                        )
                else:
                    print(
                        "You are trying to edit photo in message that doesnt have photo"
                    )

                return

            except Exception as e:
                print(f"Exception during sending message - {e}")

        # Send new message
        if photo is None:
            self.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
        else:
            self.bot.send_photo(
                chat_id=chat_id,
                caption=text,
                photo=photo,
                reply_markup=reply_markup,
            )