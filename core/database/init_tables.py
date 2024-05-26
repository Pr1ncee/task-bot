import asyncio
import logging
from sqlalchemy import text

from core.database.init_session import engine
from core.log import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

create_user_table_query = """
CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE,
    username VARCHAR NOT NULL UNIQUE,
    name VARCHAR NOT NULL
);
"""

create_task_table_query = """
CREATE TABLE IF NOT EXISTS "task" (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description VARCHAR(256),
    is_completed BOOLEAN DEFAULT FALSE,
    owner_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE
);
"""


async def create_tables() -> None:
    """
    Создаем таблицы с помощью сырых SQL запросов.
    """
    async with engine.begin() as conn:
        logger.info("Создаем таблицы...")
        await conn.execute(text(create_user_table_query))
        await conn.execute(text(create_task_table_query))
        logger.info("Таблицы успешно созданы!")


if __name__ == "__main__":
    asyncio.run(create_tables())
