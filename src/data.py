from telebot import TeleBot
import mongoengine as me



class Data:


    def __init__(self, conn_string: str, bot: TeleBot):
        self.bot = bot

        me.connect(host=conn_string)
        print("connection success ")
        self.add_quizes()

    def add_quizes(self):
        if len(Quiz.objects) == 0:
            self._add_start_quiz()
        else:
            self.update_quiz_table()


    def _add_start_quiz(self):

        quiz = Quiz(name="StartQuiz", is_required=True)

        q_name_surname = Question(
            name="name_surname",
            message="Тоді будемо знайомитися.\nЯк тебе звати?",
            correct_answer_message="Чудово, команда BTW вітає тебе!😍",
            wrong_answer_message="Введи ім’я текстом 🤡",
        )

        q_age = Question(
            name="age",
            message="Скільки тобі років?",
            regex="[1-9][0-9]",
            correct_answer_message="Ого, ми однолітки🙈",
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
            correct_answer_message="Клас🔥",
            wrong_answer_message="Обери або введи назву навчального закладу текстом  🤡",
        )

        q_study_term = Question(
            name="study_term",
            message="На якому курсі?",
            buttons=[
                "Перший",
                "Другий",
                "Третій",
                "Четвертий",
                "На магістратурі",
                "Нічого з переліченого",
            ],
            allow_user_input=False,
            correct_answer_message="Ідеальний час, щоб дізнатися щось нове🤩",
            wrong_answer_message="Вибери, будь ласка, один з варіантів 🤡",
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
            message="Ми на фінішній прямій. Вкажи адресу своєї електронної пошти. Обіцяємо, спамити не будемо😉",
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
            message="Реєстрація успішно завершена🎉 ️\n\n Дякуємо, що обрав BTW X❤️\nЧекаємо тебе на тренінгах та шерінгах.\n\n Долучайся до нашого чату з спікерами: https://t.me/joinchat/fa4V6BaBQB45Zjhi \n<b>Поонлайнимо?</b> 🤓",
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
            q_contact,
            q_email,
            q_agree,
            q_register_end,
        ]

        quiz.save()


    def update_quiz_table(self):
        quizes = Quiz.objects

        # form paragraphs in questions
        for quiz in quizes:
            for question in quiz.questions:
                question.message = question.message.replace("\\n", "\n")

            quiz.save()


class User(me.Document):
    chat_id = me.IntField(required=True, unique=True)
    name = me.StringField(required=True)
    surname = me.StringField(required=True)
    username = me.StringField(required=True)
    additional_info = me.DictField(default=None)
    registration_date = me.DateTimeField(required=True)
    register_source = me.StringField(default="Unknown")
    last_update_date = me.DateTimeField(required=True)
    last_interaction_date = me.DateTimeField(required=True)
    is_blocked = me.BooleanField(default=False)


class Question(me.EmbeddedDocument):
    name = me.StringField(required=True)
    message = me.StringField(required=True)
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
