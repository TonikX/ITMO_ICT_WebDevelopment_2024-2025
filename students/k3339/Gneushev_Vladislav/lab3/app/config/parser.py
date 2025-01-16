import os
from dataclasses import MISSING, fields, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Optional, Type, TypeVar

from dotenv import load_dotenv

T = TypeVar("T")


def cast_value(value: str, to_type: Type[T]) -> T:
    if to_type == bool:
        return value.lower() in ["true", "1", "yes"]
    elif to_type == int:
        return int(value)
    elif to_type == float:
        return float(value)
    elif to_type == str:
        return value
    elif issubclass(to_type, Enum):
        return to_type(value)
    return value


def load_config(
    config_class: Type[T],
    env_file_path: str = ".env",
    parent_prefix: Optional[str] = None,
) -> T:
    load_dotenv(dotenv_path=Path(env_file_path))

    config_values = {}

    for field in fields(config_class):
        if parent_prefix:
            env_name = f"{parent_prefix}__{field.name.upper()}"
        else:
            env_name = f"{field.name.upper()}"

        field_type = field.type
        if is_dataclass(field_type):
            nested_prefix = (
                field.name.upper()
                if not parent_prefix
                else f"{parent_prefix}__{field.name.upper()}"
            )
            config_values[field.name] = load_config(
                field_type, env_file_path, nested_prefix
            )
        else:
            env_value = os.getenv(env_name, None)
            if env_value is not None:
                config_values[field.name] = cast_value(env_value, field_type)
            else:
                if field.default != MISSING:
                    config_values[field.name] = field.default
                elif (
                    field.default_factory != MISSING
                ):  # For fields with default_factory
                    config_values[field.name] = field.default_factory()
                else:
                    config_values[field.name] = None

    return config_class(**config_values)
