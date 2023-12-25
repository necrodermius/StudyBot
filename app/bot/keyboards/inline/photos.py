from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_photos_inline_markup(query: str, id: int, markup: InlineKeyboardMarkup = None) -> InlineKeyboardMarkup:
    if not markup:
        markup = InlineKeyboardMarkup(row_width=2)

    query = query + str(id)

    markup.row(InlineKeyboardButton('Переглянути прикріплені фотографії', callback_data=f'{query}_photos'))

    return markup


def get_delete_photo_inline_markup(query: str, id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()

    query = query + str(id)

    markup.row(InlineKeyboardButton('☢ Видалити', callback_data=f'{query}_delete'))
    markup.row(InlineKeyboardButton('❌ Відмінити', callback_data=f'{query}_cancel'))

    return markup

