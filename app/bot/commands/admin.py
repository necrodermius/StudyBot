from telebot.types import BotCommand, BotCommandScopeChat, BotCommandScope

from .default import get_default_commands
from ..loader import bot


def get_admin_commands(user_id: int, chat_id: int = None) -> list[BotCommand]:
    commands = get_default_commands()

    commands.extend([
        BotCommand('/add', 'Додати домашнє завдання'),
        BotCommand('/edit', 'Редагувати домашнє завдання'),
        BotCommand('/add_file', 'Додати файл в інформацію по предмету'),
        BotCommand('/users_list', 'Отримати список користувачів'),
        BotCommand('/get_file_id', 'Отримати id файлу'),
        BotCommand('/cancel', 'Відмінити поточну дію'),
    ])

    if user_id == chat_id:
        return commands

    commands.extend([
        BotCommand('/get_id', 'Отримати id повідомлення (id прийде в особисті)'),
        BotCommand('/delete', 'Видалити повідомлення бота'),
        BotCommand('/call_all', 'Покликати всіх учасників групи')
    ])

    return commands


def set_admin_commands(user_id: int, chat_id: int = None):
    commands = get_admin_commands(user_id, chat_id)

    if user_id == chat_id:
        return bot.set_my_commands(commands, scope=BotCommandScopeChat(chat_id))

    bot.set_my_commands(commands, scope=BotCommandScope('chat_member', chat_id, user_id))
