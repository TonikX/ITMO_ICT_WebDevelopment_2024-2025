from typing import Iterable

from adaptix import P, Provider
from adaptix.conversion import get_converter

from app.domain.entities.base import EntityT


def from_db_to_entity(db_obj, entity_cls: type[EntityT], options: Iterable[Provider] = None) -> EntityT:
    converter = get_converter(
        src=type(db_obj),
        dst=entity_cls,
        recipe=options
    )
    return converter(db_obj)


def from_entity_to_db(entity_obj: EntityT, db_cls: type, options: Iterable[Provider] = None) -> type:
    converter = get_converter(
        src=type(entity_obj),
        dst=db_cls,
        recipe=options
    )
    return converter(entity_obj)
