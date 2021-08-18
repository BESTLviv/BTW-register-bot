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
