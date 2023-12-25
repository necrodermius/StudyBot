from datetime import datetime

from telebot.types import Message, CallbackQuery

from app.models import Task
from app.services.tasks import get_tasks_between_created_date
from ...base import base, callback_query_base
from ...helpers import send_message_private
from ...keyboards.inline import get_update_inline_markup
from ...loader import bot, bot_username


@bot.message_handler(regexp='^📝 Домашнє завдання задане сьогодні$')
@bot.message_handler(commands=['today_homework'])
@base()
def today_homework_handler(message: Message):
    text, markup = _get_today_homework_data()

    send_message_private(message, text, reply_markup=markup, disable_web_page_preview=True)


def _get_text(tasks: list[Task]):
    deep_link = f'tg://resolve?domain={bot_username}&start=task'

    if not tasks:
        return 'Сьогодні нічого не задали'

    text = 'Сьогодні задали:\n'
    for j in range(len(tasks)):
        task = tasks[j]
        if task.subject:
            files_view_link = f'\n<a href="{deep_link}{task.id}">Подивитись прикріплені файли 👀</a>\n' \
                if task.files or task.photos else ''

            text += f'{j + 1}) <b>{task.subject.name}<a href="{deep_link}{task.id}">⠀</a></b>\n' \
                    f'{task.text.rstrip()}{files_view_link}\n\n'

    text = text.rstrip()

    return text


@bot.callback_query_handler(func=lambda call: call.data.startswith('today_homework_'))
@callback_query_base()
def inline_today_homework_handler(call: CallbackQuery):
    option = call.data[15:]
    if option == 'update':
        text, markup = _get_today_homework_data()

        try:
            if call.inline_message_id:
                bot.edit_message_text(text, message_id=call.inline_message_id, inline_message_id=call.inline_message_id,
                                      reply_markup=markup,
                                      disable_web_page_preview=True)
            else:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup,
                                      disable_web_page_preview=True)
            bot.answer_callback_query(call.id, 'Ок')
        except Exception as e:
            if e.error_code == 400:
                bot.answer_callback_query(call.id, 'Нічого не змінилось', show_alert=True)


def _get_today_homework_data():
    now = datetime.today()
    date_from = now.replace(hour=0, minute=0, second=0, microsecond=0)
    date_to = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    tasks = get_tasks_between_created_date(date_from, date_to)

    text = _get_text(tasks)

    markup = get_update_inline_markup('today_homework')

    return text, markup
