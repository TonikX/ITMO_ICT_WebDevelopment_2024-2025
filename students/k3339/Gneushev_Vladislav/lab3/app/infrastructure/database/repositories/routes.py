from sqlalchemy import select, delete, func

from app.domain.entities.routes import Route
from app.infrastructure.database.converters.routes import from_route_db_to_dm, from_route_dm_to_db
from app.infrastructure.database.models import RouteDB
from app.infrastructure.database.repositories.base import BaseRepository


class RouteRepository(BaseRepository):
    async def get_routes(self) -> list[Route]:
        q = select(RouteDB)
        result = await self.session.execute(q)
        routes = result.scalars().all()
        return [
            from_route_db_to_dm(route)
            for route in routes
        ]

    async def add_route(self, route: Route) -> Route:
        db_model = from_route_dm_to_db(route)
        self.session.add(db_model)
        await self.session.commit()
        await self.session.refresh(db_model)
        return from_route_db_to_dm(db_model)

    async def get_route_by_id(self, route_id: int) -> Route | None:
        q = select(RouteDB).where(RouteDB.id == route_id)
        result = await self.session.execute(q)
        route = result.scalars().first()
        if route:
            return from_route_db_to_dm(route)

    async def delete_route(self, route_id: int) -> None:
        q = delete(RouteDB).where(RouteDB.id == route_id)
        await self.session.execute(q)
        await self.session.commit()

    async def get_total_length(self) -> int:
        q = select(func.sum(RouteDB.length_km))
        result = await self.session.execute(q)
        return result.scalar()

