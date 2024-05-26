"""
Модуль инициализирует кнопки постоянного меню, а также создает объект меню ReplyKeyboardMarkup.
"""
from pyrogram.types import KeyboardButton, ReplyKeyboardMarkup

menu_buttons = (
    (
        KeyboardButton("Создать задачу"),
        KeyboardButton("Мои задачи"),
    ),
)

main_menu = ReplyKeyboardMarkup(menu_buttons, resize_keyboard=True)
