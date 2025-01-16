from datetime import time

from app.domain.entities.routes import Route
from app.infrastructure.database.models import RouteDB


def from_route_db_to_dm(model: RouteDB) -> Route:
    return Route(
        id=model.id,
        name=model.name,
        start_point_name=model.start_point_name,
        end_point_name=model.end_point_name,
        start_time=time.fromisoformat(model.start_time),
        end_time=time.fromisoformat(model.end_time),
        interval_seconds=model.interval_seconds,
        duration_seconds=model.duration_seconds,
        length=model.length_km
    )


def from_route_dm_to_db(model: Route) -> RouteDB:
    return RouteDB(
        id=model.id,
        name=model.name,
        start_point_name=model.start_point_name,
        end_point_name=model.end_point_name,
        start_time=model.start_time.strftime("%H:%M"),
        end_time=model.end_time.strftime("%H:%M"),
        interval_seconds=model.interval_seconds,
        duration_seconds=model.duration_seconds,
        length_km=model.length
    )
