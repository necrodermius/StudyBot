from telebot.types import Message

from app.models import User
from ...base import base
from ...helpers import send_message_private
from ...keyboards.inline import get_help_inline_markup
from ...loader import bot


@bot.message_handler(regexp='^🆘 Допомога$')
@bot.message_handler(commands=['help'])
@base()
def help_handler(message: Message, current_user: User):
    text = '\n'.join(
        ('🆘 Інформація\n',
         '/info - Дізнатись інформацію по предмету',
         '/schedule - Дізнатись розклад',
         '/homework - Дізнатись домашнє завдання',
         '/today_homework - Дізнатись домашнє завдання, які задали сьогодня',
         '/current_info - Дізнатись, скільки часу залишилось до кінця пари и яка пара буде наступна\n',
         '/help - Допомога по боту',
         '/keyboard - Підключити клавіатуру',
         '/keyboard_off - Відключити клавіатуру\n'))
    reply_markup = None

    if current_user.is_admin():
        text += '\n'.join(
            ('\n👑 Інформація для адміністраторів\n',
             '<i>Домашнє завданнє можна додавати по швидкому шаблону</i>',
             '<pre>!Назва предмету - завадання</pre>\n',
             '/add - Додати домашнє завдання',
             '/edit - Змінитт домашнє задання\n',
             '/add_file - Додати файл в інформацію по предмету\n',
             '/users_list - Отримати список користувачів\n',
             '/get_id - Отримати id повідомлення (id прийде в особисті)',
             '/get_file_id - Отримати id файлу',
             '/delete - Видалити повідомлення боту',
             '/call_all - Покликати всіх участників групи\n')
        )

    markup = get_help_inline_markup(current_user.is_admin())

    send_message_private(message, text, reply_markup=markup)
