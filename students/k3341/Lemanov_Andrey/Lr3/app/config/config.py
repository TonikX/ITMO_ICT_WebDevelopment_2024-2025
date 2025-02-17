import os
import yaml
from pydantic import BaseModel, ValidationError
from typing import List


class AppConfig(BaseModel):
    PROJECT_NAME: str = 'peer-review'
    VERSION: str = '0.1.0'
    DOCS_URL: str = '/docs'
    OPENAPI_URL: str = '/openapi.json'
    ALLOW_ORIGINS: List[str] = ['*']
    PROPHET: bool = False
    CATBOOST: bool = True


class LoggerConfig(BaseModel):
    CONSOLE_LOG_LEVEL: str = 'DEBUG'
    FILE_LOG_LEVEL: str = 'DEBUG'


class JWTConfig(BaseModel):
    SECRET_KEY: str = "secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


class DatabaseConfig(BaseModel):
    DATABASE_URL: str = f"postgresql+asyncpg://andrey:Weroset64@localhost:5432/wallet_db"


class Config(BaseModel):
    app: AppConfig = AppConfig()
    logger: LoggerConfig = LoggerConfig()
    jwt: JWTConfig = JWTConfig()
    database: DatabaseConfig = DatabaseConfig()


def replace_env_vars(yaml_dict, default_config):
    for key, value in yaml_dict.items():
        if isinstance(value, dict):
            if key in default_config.__fields__:
                replace_env_vars(value, getattr(default_config, key))
        elif isinstance(value, str) and value.startswith('${') and value.endswith('}'):
            env_var = value[2:-1]
            default_value = getattr(default_config, key, value)
            env_value = os.getenv(env_var, default_value)
            yaml_dict[key] = env_value


def load_config(yaml_file_path: str) -> Config:
    if not os.path.exists(yaml_file_path):
        print(f"Configuration file '{yaml_file_path}' not found")
        return Config()
    with open(yaml_file_path, 'r') as file:
        config_dict = yaml.safe_load(file)
    default_config = Config()
    replace_env_vars(config_dict, default_config)
    try:
        config = Config.parse_obj(config_dict)
    except ValidationError as e:
        print("Configuration validation error:", e)
        raise
    return config


yaml_file_path = 'app/config/yaml/dev.yaml'

config = load_config(yaml_file_path)
