from telebot.types import BotCommandScopeDefault, BotCommand

from ..loader import bot


def get_default_commands() -> list[BotCommand]:
    commands = [
        BotCommand('/info', 'Дізнатися інформацію по предмету'),
        BotCommand('/schedule', 'Дізнатись розклад'),
        BotCommand('/homework', 'Дізнатись домашнє завдання'),
        BotCommand('/today_homework', 'Дізнатись домашнє завдання, яке задали сьогодні'),
        BotCommand('/current_info', 'Дізнатись, скільки часу залишилось до кінця пари, та скільки часу до наступної пари'),
        BotCommand('/help', 'Допомога по боту'),
        BotCommand('/keyboard', 'Підключити клавіатуру'),
        BotCommand('/keyboard_off', 'Відключити клавіатуру'),
    ]

    return commands


def set_default_commands():
    commands = get_default_commands()

    bot.set_my_commands(commands, scope=BotCommandScopeDefault())
