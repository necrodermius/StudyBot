from datetime import datetime, date, timedelta, time

import humanize
from telebot.types import Message, CallbackQuery

from app.services.timetable import get_subjects_by_date
from ...base import base, callback_query_base
from ...helpers import send_message_private, mark_user
from ...keyboards.inline import get_update_inline_markup
from ...loader import bot, current_app


@bot.message_handler(regexp='^❓ Яка зараз пара')
@bot.message_handler(commands=['current_info'])
@base()
def current_info_handler(message: Message):
    text, markup = _get_current_info_data()

    send_message_private(message, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('current_info'))
@callback_query_base()
def inline_homework_handler(call: CallbackQuery):
    query, option = call.data.split('current_info_')
    if option == 'update':
        text = _get_text()

        if not call.inline_message_id and call.message.chat.type != 'private':
            text = mark_user(text, call.from_user.id)

        markup = get_update_inline_markup('current_info')
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


def _get_text():
    text = ''
    current_datetime = datetime.now()
    checking_datetime = datetime.combine(date.today(), time(8, 30))

    humanize.i18n.activate(current_app.config['LOCATE'])

    subjects = get_subjects_by_date(current_datetime.date())

    if not subjects:
        return 'Сьогодні вихідний, гуляєм 🥳'

    if current_datetime < checking_datetime:
        time_to_end = checking_datetime - current_datetime
        humanize_time_to_end = humanize.precisedelta(time_to_end, minimum_unit='minutes', format='%0.0f')

        text = (f'Перша пара <b>{subjects[0].name}</b>'
                + (f' ({subjects[0].audience})\n' if subjects[0].audience else '\n') +
                f'\nДо початку залишилось ще <b>{humanize_time_to_end}</b>')

        return text

    for i in range(len(subjects)):
        if checking_datetime < current_datetime < checking_datetime + timedelta(minutes=75):
            time_to_end = (checking_datetime + timedelta(minutes=75)) - current_datetime
            humanize_time_to_end = humanize.precisedelta(time_to_end, minimum_unit='minutes', format='%0.0f')

            text = (f'Зараз: <b>{subjects[i].name}</b>'
                    + (f' ({subjects[i].audience})\n' if subjects[i].audience else '\n') +
                    f'До кінця залишилось ще <b>{humanize_time_to_end}</b>\n\n')

            if i < len(subjects) - 1:
                text += f'Наступна пара: <b>{subjects[i + 1].name}</b>' \
                        + f' ({subjects[i + 1].audience})\n' if subjects[i + 1].audience else '\n'
            else:
                text += 'Остання пара між іншим 🥳'

            break

        checking_datetime += timedelta(minutes=75)
        if i == len(subjects) - 1:
            break

        if checking_datetime < current_datetime < checking_datetime + timedelta(minutes=10):
            time_to_end = (checking_datetime + timedelta(minutes=10)) - current_datetime
            humanize_time_to_end = humanize.precisedelta(time_to_end, minimum_unit='minutes', format='%0.0f')

            text = ('Зараз перерва\n'
                    f'До кінця залишилось ще <b>{humanize_time_to_end}</b>\n\n'
                    f'Наступна пара: <b>{subjects[i + 1].name}</b>'
                    + f' ({subjects[i + 1].audience})' if subjects[i + 1].audience else '')

            break
        checking_datetime += timedelta(minutes=10)

    if not text:
        return 'Сьогодні пар більше не буде, гуляєм 🥳'

    return text.rstrip()


def _get_current_info_data():
    text = _get_text()
    markup = get_update_inline_markup('current_info')

    return text, markup
