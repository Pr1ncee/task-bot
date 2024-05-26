from enum import Enum, unique
from functools import lru_cache
from operator import attrgetter
from typing import Tuple


@unique
class BaseEnum(Enum):
    """
    Общий enum, реализующий в себе методы получения ключей и значений для более удобной работы с ним.
    Также применяется LRU-кэш для оптимизации запросов
    И декоратор 'unique', чтобы убедиться, что все значения в enum уникальны.
    """
    @classmethod
    @lru_cache(None)
    def values(cls) -> Tuple:
        return tuple(map(attrgetter("value"), cls))

    @classmethod
    @lru_cache(None)
    def names(cls) -> Tuple:
        return tuple(map(attrgetter("name"), cls))
