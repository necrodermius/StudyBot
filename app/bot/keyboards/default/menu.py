from telebot.types import ReplyKeyboardMarkup


def get_menu_keyboard_markup(is_admin: bool = False) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=2)

    markup.row('📝 Домашнє завдання задане сьогодні')
    markup.row('📃 Розклад', '📝 Домашнє завдання')
    markup.row('📚 Інформація', '❓ Яка зараз пара')
    markup.row('🆘 Допомога')

    if is_admin:
        markup.add('➕ Додати', '✏ Редагувати')
        markup.add('📑 Додати файл в інформацію')

    return markup
