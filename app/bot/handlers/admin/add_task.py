from html import escape

from telebot.types import Message

from app.models import User
from app.services.subjects import recognize_subject
from app.services.tasks import add_task
from .add_file import get_file_handler
from ...base import base
from ...helpers import send_message_private
from ...keyboards.default import get_menu_keyboard_markup, get_cancel_keyboard_markup
from ...keyboards.default import get_subjects_keyboard_markup
from ...loader import bot


@bot.message_handler(regexp='^➕ Додати$')
@bot.message_handler(commands=['add'])
@base(is_admin=True)
def add_task_handler(message: Message):
    text = 'Оберіть предмет в меню 👇'

    response = send_message_private(message, text, reply_markup=get_subjects_keyboard_markup())

    bot.register_next_step_handler(response, get_subject_handler)


@base(is_admin=True)
def get_subject_handler(message: Message):
    if message.content_type != 'text':
        response = bot.reply_to(message, f'Це {message.content_type}, а мені потрібна назва предмету!')
        return bot.register_next_step_handler(response, get_subject_handler)

    subject = recognize_subject(message.text)

    text = f'Напишіть завдання для предмету: <b>{subject.name}</b>'

    response = send_message_private(message, text, reply_markup=get_cancel_keyboard_markup())
    bot.register_next_step_handler(response, add_task_handler, subject=subject.to_json())


@base(is_admin=True)
def add_task_handler(message: Message, subject: dict, current_user: User):
    if message.content_type != 'text':
        response = bot.reply_to(message, f'Це {message.content_type}, а мені потрібне завдання для предмету!')
        return bot.register_next_step_handler(response, add_task_handler, subject=subject, current_user=current_user)

    task = add_task(subject['codename'], escape(message.text))
    if not task:
        return send_message_private(message,
                                    f'<b>Не вдалось додати завдання!</b>\nСхоже предмету "<i>{subject["name"]}</i>" немає у розкладі',
                                    reply_markup=get_menu_keyboard_markup(current_user.is_admin()))

    text = ('Додано:\n'
            f'{subject["name"]} - {task.text}')

    send_message_private(message, text)

    response = send_message_private(message, 'Відправте файл завдання', reply_markup=get_cancel_keyboard_markup())
    bot.register_next_step_handler(response, get_file_handler, _task=task.to_json())


@bot.message_handler(regexp='^!(.+)-(.|\s)+$')
@base(is_admin=True)
def add_task_via_decorator_handler(message: Message, current_user: User):
    query = message.text.replace('!', '').strip()
    subject_name = query.split('-')[0]
    task_text = query.replace(subject_name, '', 1).replace('-', '', 1).strip()

    subject = recognize_subject(subject_name)

    task = add_task(subject.codename, escape(task_text))
    if not task:
        return send_message_private(message,
                                    f'<b>Не вдалось додати завдання!</b>\nСхоже предмету "<i>{subject.name}</i>" немає у розкладі',
                                    reply_markup=get_menu_keyboard_markup(current_user.is_admin()))

    text = ('Додано:\n'
            f'<b>{subject.name}</b> - {task.text}')

    bot.send_message(message.chat.id, text, parse_mode='HTML')
