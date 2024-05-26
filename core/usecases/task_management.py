import logging
from typing import AsyncGenerator

from pyrogram.types import Message, CallbackQuery
from transitions.core import MachineError

from core.keyboards.reply_keyboard import main_menu
from core.keyboards.inline_keyboard import get_tasks_buttons, get_delete_button
from database.init_session import async_db_session
from fsm.state_machine import StateMachine
from log import setup_logging
from adapters.repositories.task_repository import TaskRepository
from usecases.user_management import UserUseCase
from utils import get_user_state

setup_logging()
logger = logging.getLogger(__name__)


class TaskUseCase:
    """
    Класс, реализующий в себе всю бизнес-логику приложения для сущности Task
    """
    def __init__(self, session: AsyncGenerator = async_db_session) -> None:
        self.session = session

    @staticmethod
    async def get_task_title(message: Message, user_state: StateMachine) -> None:
        """
        Метод, получающий нозвание задачи из пользовательского ввода и сохраняющий его в user_state.
        :param message: объект сообщения пользователя
        :param user_state: текущее состояние пользователя в Конечном Автомате
        """
        task_title = message.text
        logger.info(f"Пользователь ввел название задачи ({task_title}).")
        user_state.task_title = task_title
        user_state.get_task_title()
        await message.reply("Введите описание задачи.")

    @staticmethod
    def get_task_description(message: Message, user_state: StateMachine) -> str:
        """
        Метод, получающий описание задачи из пользовательского ввода.
        :param message: объект сообщения пользователя
        :param user_state: текущее состояние пользователя в Конечном Автомате
        :return: описание задачи в строковом формате
        """
        task_desc = message.text
        logger.info(f"Пользователь ввел описание задачи ({task_desc}).")
        user_state.get_task_description()
        return task_desc

    async def create_task(self, message: Message, user_state: StateMachine) -> None:
        """
        Метод, создающий задачу.
        :param message: объект сообщения пользователя
        :param user_state: текущее состояние пользователя в Конечном Автомате
        """
        user_id = message.from_user.id
        task_title = user_state.task_title
        task_description = self.get_task_description(message=message, user_state=user_state)

        logger.info(f"Создаем новую задачу для пользователя <{user_id}> с названием - {task_title}...")
        await TaskRepository(session=self.session).create_task(
            user_id=user_id,
            task_title=task_title,
            task_desc=task_description
        )
        logger.info(f"Задача с названием <{task_title}> успешно создана!")
        await message.reply("Задача успешно создана!", reply_markup=main_menu)

    async def init_task_creation(
            self,
            user_id: int,
            local_state: dict,
            message: Message
    ) -> None:
        """
        Метод, инициирующий создание задачи путем изменения состояния.
        :param user_id: уникальный ID пользователя в Telegram
        :param local_state: локальное хранилище состояний в Конечном Автомате
        :param message: объект сообщения пользователя
        """
        # Пользователь должен быть обязательно зарегистрирован
        user = await UserUseCase().is_user_registered(user_id=user_id)
        if user:
            try:
                user_state = get_user_state(user_id=user_id, local_state=local_state)
                user_state.create_task()
                logger.info(f"Начинаем создавать задачу для пользователя <{user_id}>...")
                await message.reply("Введите название задачи.")
            except MachineError as e:
                logger.error(f"Возникла ошибка при переходе между состояниями конечного автомата! Ошибка: {e}")
                await message.reply("Пожалуйста, закончите предыдущее действие.")
        else:
            logger.warning(f"Незаригистрированный пользователь <{user_id}> хочет создать задачу!")
            await message.reply("Пожалуйста, сначала зарегистрируйтесь, введя команду /start.")

    async def view_tasks(self, message: Message) -> None:
        """
        Методы, реализующий логику для просмотра задач пользователя.
        :param message: объект сообщения пользователя
        """
        user_id = message.from_user.id
        # Пользователь должен быть обязательно зарегистрирован
        user = await UserUseCase().is_user_registered(user_id=user_id)
        if user:
            tasks = await TaskRepository(session=self.session).get_user_tasks(user_id=user_id)
            logger.info(f"Задачи пользователя <{user_id}>: {tasks}")
            if tasks:
                for task in tasks:
                    if not task.is_completed:  # Проверяем, выполнена ли задача
                        task_buttons = get_tasks_buttons(task_id=task.id)
                        await message.reply(
                            f"Задача: {task.title}\nОписание: {task.description}",
                            reply_markup=task_buttons
                        )
                    else:  # Если да, выводим определенный текст и кнопку "Удалить"
                        delete_button = get_delete_button(task_id=task.id)
                        await message.reply(
                            f'Задача "{task.title}" выполнена ✅',
                            reply_markup=delete_button
                        )
            else:
                await message.reply("У вас нет задач.")
        else:
            logger.warning(f"Незаригистрированный пользователь <{user_id}> хочет просмотреть свои задачи!")
            await message.reply("Пожалуйста, сначала зарегистрируйтесь, введя команду /start.")

    async def delete_task(self, task_id: int, callback_query: CallbackQuery) -> None:
        """
        Метод, удаляющий задачу по ID задачи в Базе Данных.
        :param task_id: уникальный ID задачи в Базе Данных
        :param callback_query: объект обратного вызова с помощью кнопкии на встроенной клавиатуре
        """
        await TaskRepository(session=self.session).delete_task(task_id=task_id)
        logger.info(f"Задача <{task_id}> удалена.")
        await callback_query.message.edit_text("Задача удалена.")

    async def set_task_completed(self, task_id: int, callback_query: CallbackQuery) -> None:
        """
        Метод, устанавливающий статус 'выполнена' на задачу с указанным ID.
        :param task_id: уникальный ID задачи в Базе Данных
        :param callback_query: объект обратного вызова с помощью кнопкии на встроенной клавиатуре
        """
        task_repository = TaskRepository(session=self.session)
        await task_repository.set_task_completed(task_id=task_id)
        task = await task_repository.get_task(task_id=task_id)

        delete_button = get_delete_button(task_id=task.id)
        logger.info(f"Задача <{task_id}> теперь выполнена.")
        await callback_query.message.edit_text(
            f'Задача "{task.title}" выполнена ✅',
            reply_markup=delete_button
        )
