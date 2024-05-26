"""
Модуль для импортирования переменных окружения, а также для общих настроек приложения, логически разделенным по классам.
"""
import os

from dotenv import load_dotenv

load_dotenv()


class PostgresConfig:
    HOST = os.getenv("POSTGRES_HOST", "localhost")
    PWD = os.getenv("POSTGRES_PASSWORD", "postgres")
    USER = os.getenv("POSTGRES_USER", "postgres")
    NAME = os.getenv("POSTGRES_DB", "tasks_bot")
    PORT = os.getenv("POSTGRES_PORT", "5432")
    DATABASE_URL = f"postgresql+asyncpg://{USER}:{PWD}@{HOST}:{PORT}/{NAME}"


class BotConfig:
    NAME = "Tasks Bot"
    API_ID = os.getenv("API_ID", "123")
    API_HASH = os.getenv("API_HASH", "abc123")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "abcd:1234")


bot_config = BotConfig()
postgres_config = PostgresConfig()
