from dataclasses import dataclass
from typing import TypeVar


@dataclass
class Entity:
    """
    Базовый класс для всех сущностей
    """


EntityT = TypeVar("EntityT", bound=Entity)
