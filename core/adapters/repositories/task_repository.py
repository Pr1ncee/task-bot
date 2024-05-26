from typing import AsyncGenerator, List

from sqlalchemy import text, Row

from adapters.repositories.base_repository import BaseRepository


class TaskRepository(BaseRepository):
    """
    Репозиторий, реализующий общие методы для взаимодействия с таблицей 'task' в Базе Данных.
    Параметризированные запросы нужны для предотвращения SQL-инъекнций.
    """
    def __init__(self, session: AsyncGenerator) -> None:
        super().__init__(session)
        self.session = session

    async def create_task(self, user_id: int, task_title: str, task_desc: str) -> None:
        """
        Метод, создающий новую задачу с указанными параметрами.
        :param user_id: уникальный ID пользователя в Telegram
        :param task_title: нозвание задачи
        :param task_desc: описание задачи
        """
        insert_task_query = text(
            """
            INSERT INTO "task" (title, description, owner_id)
            VALUES (:task_title, :task_desc, (SELECT id FROM "user" WHERE user_id = :user_id))
            """
        )
        params = {'task_title': task_title, 'task_desc': task_desc, 'user_id': user_id}
        await self._execute_commit(query=insert_task_query, params=params)

    async def get_user_tasks(self, user_id: int) -> List[Row]:
        """
        Метод, получающий все задачи для определенного пользователя.
        :param user_id: уникальный ID пользователя в Telegram
        :return: массив (лист) с объектами Row, которые представляют собой запись в таблице
        """
        get_task_query = text(
            """
            SELECT id, title, description, is_completed
            FROM "task"
            WHERE owner_id = (SELECT id FROM "user" WHERE user_id = :user_id)
            """
        )
        tasks = await self._execute_commit(query=get_task_query, params={'user_id': user_id}, commit=False)
        return tasks.fetchall()

    async def delete_task(self, task_id: int) -> None:
        """
        Метод, удаляющий задачу.
        :param task_id: уникальный ID задачи в Базе Данных
        """
        delete_task_query = text(
            """
            DELETE FROM "task"
            WHERE id = :task_id
            """
        )
        await self._execute_commit(query=delete_task_query, params={'task_id': task_id})

    async def set_task_completed(self, task_id: int) -> None:
        """
        Метод, обновляющий статус задачи на 'выполнена' (обновляет 'is_completed' поле в таблице на TRUE).
        :param task_id: уникальный ID задачи в Базе Данных
        """
        update_task_query = text(
            """
            UPDATE "task"
            SET is_completed = TRUE
            WHERE id = :task_id
            """
        )
        await self._execute_commit(query=update_task_query, params={'task_id': task_id})

    async def get_task(self, task_id: int) -> Row:
        """
        Метод, получающий задачу по ее ID.
        :param task_id: уникальный ID задачи в Базе Данных
        :return: объект Row, представляющий результирующую строку из таблицы
        """
        get_task_query = text(
            """
            SELECT id, title
            FROM "task"
            WHERE id = :task_id
            """
        )
        task = await self._execute_commit(query=get_task_query, params={'task_id': task_id}, commit=False)
        return task.fetchone()
