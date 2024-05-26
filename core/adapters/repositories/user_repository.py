from typing import AsyncGenerator

from sqlalchemy import text

from adapters.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    """
    Репозиторий, реализующий общие методы для взаимодействия с таблицей 'user' в Базе Данных.
    Параметризированные запросы нужны для предотвращения SQL инъекнций.
    """
    def __init__(self, session: AsyncGenerator) -> None:
        super().__init__(session)
        self.session = session

    async def sign_up_user(self, user_id: int, username: str, name: str) -> None:
        """
        Метод, создающий нового пользователя с указанными параметрами
        :param user_id: уникальный ID пользователя в Telegram
        :param username: логин пользователя (уникальный)
        :param name: имя пользователя
        """
        insert_user_query = text(
            """
            INSERT INTO "user" (user_id, username, name)
            VALUES (:user_id, :username, :name)
            """
        )
        params = {'user_id': user_id, 'username': username, 'name': name}
        await self._execute_commit(query=insert_user_query, params=params)

    async def is_user_registered(self, user_id: int) -> bool:
        """
        Метод, проверящий, зарегистрирован ли данные пользователь.
        :param user_id: уникальный ID пользователя в Telegram
        :return: булеан, зарегистрирован ли пользователь
        """
        is_user_registered_query = text(
            """SELECT * FROM "user" WHERE user_id = :user_id LIMIT 1"""
        )
        result = await self._execute_commit(query=is_user_registered_query, params={"user_id": user_id})
        return result.scalar() is not None

    async def is_username_unique(self, username: str) -> bool:
        """
        Метод, проверяющий уникальность логина.
        :param username: логин в строковом формате
        :return: булеан, является ли логин уникальным
        """
        is_username_unique_query = text(
            """SELECT * FROM "user" WHERE username = :username LIMIT 1"""
        )
        result = await self._execute_commit(query=is_username_unique_query, params={"username": username})
        return result.scalar() is not None
