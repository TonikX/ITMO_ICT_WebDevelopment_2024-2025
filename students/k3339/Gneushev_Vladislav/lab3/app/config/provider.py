from dishka import Provider, Scope, from_context, provide

from app.config.models import (
    Config,
    DatabaseConfig, APIConfig, AuthConfig,
)


class ConfigProvider(Provider):
    scope = Scope.APP
    config = from_context(provides=Config, scope=Scope.APP)

    @provide
    def get_api_config(self, config: Config) -> APIConfig:
        return config.api

    @provide
    def get_db_config(self, config: Config) -> DatabaseConfig:
        return config.db

    @provide
    def get_auth_config(self, config: Config) -> AuthConfig:
        return config.auth
