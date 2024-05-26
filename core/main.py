"""
Главный модуль для запуска бота.
Инициализирует объект Клиента из pyrogram, а также различных функций для обработки пользовательских сообщений.
"""
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery

from core.config import bot_config
from usecases.task_management import TaskUseCase
from core.usecases.state_management import StateManagement
from core.utils import get_user_state

app = Client(
    name=bot_config.NAME,
    api_id=bot_config.API_ID,
    api_hash=bot_config.API_HASH,
    bot_token=bot_config.BOT_TOKEN
)
local_state = {}  # TODO Заменить локальной хранилище более надеждым, например, Redis или MongoDB


@app.on_message(filters.command("start"))
async def start(client: Client, message: Message) -> None:
    user_id = message.from_user.id
    await StateManagement().start(user_id=user_id, local_state=local_state, message=message)


@app.on_message(filters.text & filters.private & filters.regex(r"^Создать задачу$"))
async def create_task(client: Client, message: Message) -> None:
    user_id = message.from_user.id
    await TaskUseCase().init_task_creation(user_id=user_id, local_state=local_state, message=message)


@app.on_message(filters.text & filters.private & filters.regex(r"^Мои задачи$"))
async def view_tasks(client: Client, message: Message) -> None:
    await TaskUseCase().view_tasks(message)


@app.on_message(filters.text & filters.private)
async def handle_menu(client: Client, message: Message) -> None:
    user_id = message.from_user.id
    user_state = get_user_state(user_id=user_id, local_state=local_state)
    await StateManagement().handle_state_transitions(message, user_state)


@app.on_callback_query(filters.regex(r"complete_(\d+)"))
async def mark_task_completed(client: Client, callback_query: CallbackQuery) -> None:
    task_id = int(callback_query.data.split("_")[1])
    await TaskUseCase().set_task_completed(task_id=task_id, callback_query=callback_query)


@app.on_callback_query(filters.regex(r"delete_(\d+)"))
async def delete_task(client: Client, callback_query: CallbackQuery) -> None:
    task_id = int(callback_query.data.split("_")[1])
    await TaskUseCase().delete_task(task_id=task_id, callback_query=callback_query)


app.run()
