from typing import AsyncGenerator

from sqlalchemy import TextClause, CursorResult


class BaseRepository:
    """
    Репозиторий, который реализует общие методы для взаимодействия с Базой Данных
    """
    def __init__(self, session: AsyncGenerator) -> None:
        self.session = session

    async def _execute_commit(self, query: TextClause, params: dict, commit: bool = True) -> CursorResult:
        """
        Метод, выполняющий запрос в Базу Данных.
        Если указан флаг 'commit' - коммитит изменения в Базу Данных.
        :param query: запрос для выполнения
        :param params: параметры в самом SQL-запросе для предотвращения SQL инъекций
        :param commit: если True - коммитит изменения
        :return: возвращает нативный объект SQLAlchemy - CursorResult, который содержит результат выполнения запроса
                 (None или объект Row)
        """
        async for session in self.session():
            result = await session.execute(query, params)
            if commit:
                await session.commit()
            return result

