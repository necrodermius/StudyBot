from telebot.types import ReplyKeyboardMarkup


def get_enough_keyboard_markup() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add('👀 Достатньо')
    markup.add('❌ Відмінити')
    return markup
