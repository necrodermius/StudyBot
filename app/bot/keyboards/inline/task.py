from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_edit_inline_markup(query: str, id: int, markup: InlineKeyboardMarkup = None, files_button: bool = False) -> InlineKeyboardMarkup:
    if not markup:
        markup = InlineKeyboardMarkup()

    query = query + str(id)

    markup.row(InlineKeyboardButton('✏ Редагувати', callback_data=f'{query}_edit'),
               InlineKeyboardButton('☢ Видалити', callback_data=f'{query}_delete'))

    if files_button:
        markup.row(InlineKeyboardButton('➕ Додати файл', callback_data=f'{query}_files'))

    markup.row(InlineKeyboardButton('❌ Відмінити', callback_data=f'{query}_cancel'))
    return markup
