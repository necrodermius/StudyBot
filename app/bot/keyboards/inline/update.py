from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_update_inline_markup(query: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton('🔄 Оновити', callback_data=f'{query}_update'))
    return markup
