import logging
from typing import AsyncGenerator

from pyrogram.types import Message

from core.keyboards.reply_keyboard import main_menu
from database.init_session import async_db_session
from fsm.state_machine import StateMachine
from log import setup_logging
from adapters.repositories.user_repository import UserRepository

setup_logging()
logger = logging.getLogger(__name__)


class UserUseCase:
    """
    Класс, реализующий в себе всю бизнес-логику приложения для сущности User.
    """
    def __init__(self, session: AsyncGenerator = async_db_session) -> None:
        self.session = session

    async def get_name(self, message: Message, user_state: StateMachine) -> None:
        """
        Метод, получающий имя пользователя из пользовательского ввода и сохраняющий его в user_state.
        :param message: объект сообщения пользователя
        :param user_state: текущее состояние пользователя в Конечном Автомате
        """
        name = message.text
        logger.info(f"Пользователь ввел свое имя ({name}).")
        user_state.user_name = name
        user_state.get_name()
        await message.reply("Отлично! Теперь введите логин.")

    async def get_username(self, message: Message) -> None | str:
        """
        Метод, который получает логин пользователя и проверяет его на уникальность.
        :param message: объект сообщения пользователя
        :return: строку с логином пользователя, если пользователь ввел уникальный логин, иначе None
        """
        username = message.text
        username_exists = await self.is_username_unique(username=username)
        if username_exists:
            logger.warning(f"Пользователь ввел уже существующий логин ({username}).")
            await message.reply("Этот логин уже занят, попробуйте другой.")

        logger.info(f"Пользователь ввел уникальный логин ({username}).")
        return None if username_exists else username

    async def create_user(self, message: Message, user_state: StateMachine) -> None:
        """
        Методы, создающий пользователя.
        :param message: объект сообщения пользователя
        :param user_state: текущее состояние пользователя в Конечном Автомате
        """
        username = await self.get_username(message=message)
        if username:  # Не создаем нового пользователя, если логин неуникальный
            user_id = message.from_user.id
            name = user_state.user_name
            user_state.get_username()

            logger.info(f"Создаем нового пользователя с <{name}> именем и <{username}> логином...")
            await UserRepository(session=self.session).sign_up_user(user_id=user_id, username=username, name=name)
            logger.info(f"Новый пользователь успешно создан!")
            await message.reply("Регистрация завершена! Добро пожаловать.", reply_markup=main_menu)

    async def is_user_registered(self, user_id: int) -> bool:
        """
        Метод, проверяющий, зарегистрирован ли данный пользователь.
        :param user_id: уникальный ID пользователя в Telegram
        :return: булеан, зарегистрирован ли пользователь
        """
        return await UserRepository(session=self.session).is_user_registered(user_id=user_id)

    async def is_username_unique(self, username: str) -> bool:
        """
        Метод, проверяющий уникальность данного логина.
        :param username: логин в строковом формате
        :return: булеан, является ли логин уникальным
        """
        return await UserRepository(session=self.session).is_username_unique(username=username)
