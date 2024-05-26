from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_tasks_buttons(task_id: int) -> InlineKeyboardMarkup:
    """
    Функция возвращает встроенной кнопки с ассоциированным task_id для этой задачи.
    :param task_id: ID задачи в Базе Данных
    :return: объект встроенной клавиатуры InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Пометить как выполненную", callback_data=f"complete_{task_id}")],
            [InlineKeyboardButton("Удалить", callback_data=f"delete_{task_id}")]
        ]
    )


def get_delete_button(task_id: int) -> InlineKeyboardMarkup:
    """
    Функция возвращает встроенной кнопку с ассоциированным task_id для этой задачи.
    Используется для выполненных задач.
    :param task_id: ID задачи в Базе Данных
    :return: объект встроенной клавиатуры InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Удалить", callback_data=f"delete_{task_id}")]
        ]
    )
