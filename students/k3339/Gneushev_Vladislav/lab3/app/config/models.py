from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    host: str
    port: int
    user: str
    password: str
    database: str

    @property
    def uri(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class APIConfig:
    internal_host: str
    port: int
    auto_reload: bool = True
    workers: int = 1


@dataclass
class AuthConfig:
    secret_token: str
    access_token_lifetime: int


@dataclass
class Config:
    db: DatabaseConfig
    api: APIConfig
    auth: AuthConfig
