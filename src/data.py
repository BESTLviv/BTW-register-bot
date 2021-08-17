from telebot import TeleBot
import mongoengine as me
from datetime import datetime, timezone

import string
import random


class Data:

    TEST_PHOTO = "https://i.ibb.co/0Gv4JyW/photo-2021-04-16-12-48-15.jpg"

    def __init__(self, conn_string: str, bot: TeleBot):
        self.bot = bot

        me.connect(host=conn_string)
        print("connection success ")

        # if there is no ejf table in DB - then create it
        if len(BTW.objects) == 0:
            self.reinit_ejf_table()
            print("ejf and content tables have been initialized")
        # if there was table already
        else:
            self.update_ejf_table()

        self.ADMIN_PASSWORD = self.get_btw().admin_password

        # if there is no quiz table in DB - then create it
        self.add_quizes()

    def add_quizes(self):
        if len(Quiz.objects) == 0:
            self._add_start_quiz()
        # otherwise update it
        else:
            self.update_quiz_table()

    def _add_start_quiz(self):

        quiz = Quiz(name="StartQuiz", is_required=True)

        q_name_surname = Question(
            name="name_surname",
            message="Тоді будемо знайомитися.\nЯк тебе звати?",
            correct_answer_message="Чудово, команда BTW вітає тебе!",
            wrong_answer_message="Введи ім’я текстом 🤡",
        )

        q_age = Question(
            name="age",
            message="Скільки тобі років?",
            regex="[1-9][0-9]",
            correct_answer_message="Ого, ми однолітки 🥰",
            wrong_answer_message="Вкажи свій справжній вік 🤡",
        )

        q_school = Question(
            name="school",
            message="Де вчишся? Вибери або введи.",
            buttons=[
                "НУЛП",
                "ЛНУ",
                "УКУ",
                "КПІ",
                "КНУ",
                "Ще в школі",
                "Вже закінчив(-ла)",
            ],
            correct_answer_message="Клас 🥰",
            wrong_answer_message="Введи назву текстом 🤡",
        )

        q_study_term = Question(
            name="study_term",
            message="На якому курсі?",
            buttons=[
                "Перший",
                "Другий",
                "Третій",
                "Четвертий",
                "На магістартурі",
                "Нічого з переліченого",
            ],
            allow_user_input=False,
            correct_answer_message="Ідеальний час, щоб дізнатись щось нове 🥰",
            wrong_answer_message="Вибери, будь ласка, один з варіантів 🤡",
        )

        ##############
        q_city = Question(
            name="city",
            message="Звідки ти? Вибери зі списку або введи назву.",
            buttons=["Львів", "Київ", "Новояворівськ", "Донецьк", "Стамбул"],
            correct_answer_message="Був-був там!",
            wrong_answer_message="Введи назву текстом :)",
        )

        q_contact = Question(
            name="contact",
            message="Супер! Поділишся з нами своїми контактами?",
            buttons=["Тримай!"],
            input_type="contact",
            correct_answer_message="Дякую. А я залишаю тобі контакт головного організатора: @kerril 🥰",
            wrong_answer_message="Надішли, будь ласка, свій контакт 🤡",
        )

        q_email = Question(
            name="email",
            message="Ми на фінішній прямій. Вкажи адресу своєї електронної пошти. Обіцяємо, спамити не будемо)",
            regex="^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$",
            correct_answer_message="Дякую 🥰",
            wrong_answer_message="Введи, будь ласка, електронну адресу 🤡",
        )

        q_agree = Question(
            name="user_agreements",
            message="Залишилося тільки дати згоду на обробку даних.",
            buttons=["Я погоджуюсь."],
            allow_user_input=False,
        )

        q_register_end = Question(
            name="end_register",
            message="Дякуємо, що обрав BTW X❤️\n\nЧекаємо тебе на тренінгах та шерінгах.\n\n Долучайся до нашого чату з спікерами: https://t.me/joinchat/fa4V6BaBQB45Zjhi \n\n<b>Поонлайнимо?</b> 🤓",
            buttons=[
                "Звісно"
            ],
            allow_user_input=False,
        )

        quiz.questions = [
            q_name_surname,
            q_age,
            q_school,
            q_study_term,
            # q_city,           # ДУМАЮ ЩО ЦЕ ХОРОША ІДЕЯ ЗБИРАТИ МІСТА
            q_contact,
            q_email,
            q_agree,
            q_register_end,
        ]

        quiz.save()

    def reinit_ejf_table(self):
        # delete collections
        BTW.objects.delete()
        Content.objects.delete()

        # create content table
        content = Content()
        content.start_text = (
            "Привіт, любий друже!\n"
            "Насувається десятий BEST training week, тиждень мега крутих тренінгів та шерінгів🔥 Тому саме для тебе ми підготували щось дійсно захопливе. Наші спікери розкажуть тобі багато крутої інфи й поділяться власним досвідом✨\n"
            "Пройди реєстрацію і дізнайся, що на тебе чекає."
        )

        content.ejf_start_text = (
            "Я знаю, друже, що до 19 травня ще є трохи часу, тому приготував для тебе кілька корисних штук. Заходь у <b>меню</b>, читай, слідкуй за оновленнями 🧐\n\n"
            "Почувай себе, як вдома ☺️"
        )
        content.ejf_start_photo = self.TEST_PHOTO
        content.save()

        # create ejf table
        ejf = BTW()
        ejf.admin_password = "admin"
        ejf.start_menu = [  ##### Тут можна розмістити спікерів (думаю що наввіть ТРЕБА)
            SimpleButton(
                name="Що? 🤨",
                text=(
                    "<b>Інженерний ярмарок кар’єри — коротко ІЯК — це must-visit подія для кожного студента.</b> Не лякайся слова “інженерний”, бо наш Ярмарок уже давно вийшов за будь-які рамки і навіть претендує називатися наймасштабнішим у Львові.\n\n"
                    "У нас для цього є все:\n\n"
                    "✅ <b>Топ-компанії</b>, які зацікавлені в студентах. Чекни розділ 'Компанії'.\n\n"
                    "✅ Класний <b>контент</b>, який за два дні допоможе тобі нарешті відповісти на питання, ким ти хочеш стати. Ознайомся з розділом 'Розклад'.\n\n"
                    "✅ Можливість знайти <b>роботу</b> прямо через бота, тобто через мене! Після 20 травня я оновлю меню і ти все зрозумієш.\n\n"
                    "✅ Найкращі <b>учасники</b>. Угу, такі як ти!😌\n\n"
                    "Останні штрихи й ІЯК 2021 стане реальністю. Ще й не простою, а віртуальною. <b>Зустрінемося на Hopin!</b>\n\n"
                    "Па!"
                ),
                photo=self.TEST_PHOTO,
            ),
            SimpleButton(
                name="Де і як? 🦦",
                text=(
                    "Пам’ятаєш, ще на початку я казав, що ІЯК став віртуалом? Так-от, я мав на увазі, що цього року у Львівській політехніці звичного Ярмарку не буде. Не буде довгих черг, великих скупчень і хаосу. <b>Ми переїжджаємо в кращі санітарні умови... В онлайн простір!</b>✌️👩‍💻\n\n"
                    "ІЯК відбудеться на платформі <b>Hopin</b>. Ти майже не відчуєш різниці між спілкуванням наживо і онлайн. На Hopin усе організовано так, як ми звикли: віртуальні стенди з компаніями, окрема кімната для презентацій та воркшопів. Є навіть сцена!\n\n"
                    "<b>Переходь за посиланням у запрошенні і побач усе на власні очі.</b>"
                ),
                photo=self.TEST_PHOTO,
            ),
            SimpleButton(
                name="Компанії 📈",
                text="КомпаніїКомпаніїКомпанії",
                photo=self.TEST_PHOTO,
                url_link="https://ejf.best-lviv.org.ua/partners/ejfwp/",
                url_text="Детально про компанії",
            ),
            SimpleButton(
                name="Розклад 📌",
                text="РозкладРозкладРозклад",
                photo=self.TEST_PHOTO,
            ),
            SimpleButton(
                name="Зв'язок з нами ✍️",
                text=(
                    "🙂Залишилися питання? Може, маєш важливий фідбек на цьому етапі? У такому разі напиши комусь з нас🙃\n\n"
                    "<b>Вибирай:</b>\n\n"
                    "<a href='https://t.me/Slavkoooo'>головний організатор Ярік</a>\n\n"
                    "<a href='https://t.me/PogibaAnn'>відповідальна за компанії Аня</a>\n\n"
                    "<a href='https://t.me/OnAzart'>відповідальний за компанії Назар</a>\n\n"
                    "<a href='https://t.me/Yaroslav_Horodyskyi'>відповідальний за технічну частину Ярік</a>\n\n"
                    "<a href='https://t.me/demberetska'>відповідальна за контент Соля</a>\n\n"
                    "<a href='https://t.me/foxiero'>відповідальна за дизайн Софа</a>\n\n"
                    "<a href='https://t.me/vikahbhk'>відповідальна за піар Віка</a>\n\n"
                    "<a href='https://t.me/yarchik_5'>відповідальна за людські ресурси Ярина</a>\n\n"
                ),
                photo=self.TEST_PHOTO,
            ),
        ]
        ejf.content = content
        ejf.start_datetime = datetime(2021, 5, 19, 10, 0, 0)
        # ejf.end_datetime = self.JOB_FAIR_END_TIME
        ejf.save()

    def update_ejf_table(self):
        ejf = self.get_btw()

        # form paragraphs in ejf menu
        for btn in ejf.start_menu:
            btn.name = btn.name.replace("\\n", "\n")
            btn.text = btn.text.replace("\\n", "\n")

        # form paragraphs in content
        content = ejf.content
        ejf.content.start_text = content.start_text.replace("\\n", "\n")
        ejf.content.ejf_start_text = content.ejf_start_text.replace("\\n", "\n")

        ejf.content.save()
        ejf.save()

    def update_quiz_table(self):
        quizes = Quiz.objects

        # form paragraphs in questions
        for quiz in quizes:
            for question in quiz.questions:
                question.message = question.message.replace("\\n", "\n")

            quiz.save()

    def get_btw(self):
        return BTW.objects.first()


class Content(me.Document):
    start_text = me.StringField()
    start_photo = me.StringField()
    ejf_start_text = me.StringField()
    ejf_start_photo = me.StringField()


class SimpleButton(me.EmbeddedDocument):
    name = me.StringField()
    text = me.StringField()
    photo = me.StringField()
    url_link = me.StringField()
    url_text = me.StringField()


class BTW(me.Document):
    admin_password = me.StringField()
    start_menu = me.ListField(me.EmbeddedDocumentField(SimpleButton), default=list())
    content = me.ReferenceField(Content)
    start_datetime = me.DateTimeField()
    end_datetime = me.DateTimeField()


class User(me.Document):
    chat_id = me.IntField(required=True, unique=True)
    name = me.StringField(required=True)
    surname = me.StringField(required=True)
    username = me.StringField(required=True)
    interests = me.ListField(default=list())
    experience = me.ListField(default=list())
    employment = me.ListField(default=list())
    cv_file_id = me.StringField(default=None)
    cv_file_name = me.StringField(default=None)
    apply_counter = me.IntField(default=20)
    additional_info = me.DictField(default=None)
    register_source = me.StringField(default="Unknown")
    registration_date = me.DateTimeField(required=True)
    last_update_date = me.DateTimeField(required=True)
    last_interaction_date = me.DateTimeField(required=True)
    hr_status = me.BooleanField(default=False)
    is_blocked = me.BooleanField(default=False)


class Question(me.EmbeddedDocument):
    name = me.StringField(required=True)
    message = me.StringField(required=True)
    # photo = me.StringField(default=None)
    buttons = me.ListField(default=list())
    input_type = me.StringField(choices=["text", "photo", "contact"], default="text")
    max_text_size = me.IntField(max_value=4000)
    allow_user_input = me.BooleanField(default=True)
    regex = me.StringField(default=None)
    correct_answer_message = me.StringField(defaul=None)
    wrong_answer_message = me.StringField(default="Неправильний формат!")


class Quiz(me.Document):
    name = me.StringField(required=True)
    questions = me.ListField(me.EmbeddedDocumentField(Question), default=list())
    is_required = me.BooleanField(default=False)
