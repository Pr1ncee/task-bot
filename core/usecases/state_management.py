import logging
from typing import AsyncGenerator

from pyrogram.types import Message

from core.usecases.task_management import TaskUseCase
from core.usecases.user_management import UserUseCase
from database.init_session import async_db_session
from fsm.state_machine import StateMachine
from fsm.states import States
from log import setup_logging
from utils import get_user_state

setup_logging()
logger = logging.getLogger(__name__)


class StateManagement:
    def __init__(self, session: AsyncGenerator = async_db_session) -> None:
        self.session = session

    async def start(self, user_id: int, local_state: dict, message: Message) -> None:
        user = await UserUseCase().is_user_registered(user_id=user_id)
        if user:
            logger.warning("Данный пользователь уже зарегистрирован!")
            await message.reply("Вы уже зарегистрированы!")
        else:
            logger.info("Начинаем регистрацию пользователя...")
            user_state = get_user_state(user_id=user_id, local_state=local_state)
            user_state.start()
            await message.reply("Добро пожаловать! Пожалуйста, введите ваше имя.")

    async def handle_state_transitions(self, message: Message, user_state: StateMachine) -> None:
        match user_state.state:
            case States.GET_NAME.value:
                await UserUseCase().get_name(message=message, user_state=user_state)
            case States.GET_USERNAME.value:
                await UserUseCase().create_user(message=message, user_state=user_state)
            case States.GET_TASK_TITLE.value:
                await TaskUseCase.get_task_title(message=message, user_state=user_state)
            case States.GET_TASK_DESCRIPTION.value:
                await TaskUseCase().create_task(message=message, user_state=user_state)
