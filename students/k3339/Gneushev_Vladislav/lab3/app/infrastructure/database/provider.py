from typing import AsyncIterable

from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, AsyncEngine

from app.config.models import DatabaseConfig
from app.infrastructure.database.connection import create_engine, create_session_maker
from app.infrastructure.database.repositories.assignments import AssignmentRepository
from app.infrastructure.database.repositories.buses import BusRepository
from app.infrastructure.database.repositories.drivers import DriverRepository
from app.infrastructure.database.repositories.routes import RouteRepository
from app.infrastructure.database.repositories.users import UserRepository


class DatabaseProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_engine(self, config: DatabaseConfig) -> AsyncIterable[AsyncEngine]:
        engine = create_engine(config)
        yield engine
        # await engine.dispose(True)

    @provide
    def get_pool(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return create_session_maker(engine)

    @provide(scope=Scope.REQUEST)
    async def get_session(
            self, pool: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with pool() as session:
            yield session

    driver_repository = provide(DriverRepository, scope=Scope.REQUEST)
    route_repository = provide(RouteRepository, scope=Scope.REQUEST)
    assignment_repository = provide(AssignmentRepository, scope=Scope.REQUEST)
    bus_repository = provide(BusRepository, scope=Scope.REQUEST)
    user_repository = provide(UserRepository, scope=Scope.REQUEST)
