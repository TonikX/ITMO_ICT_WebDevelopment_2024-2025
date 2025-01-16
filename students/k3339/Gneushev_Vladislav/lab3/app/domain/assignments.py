from app.domain.entities.routes import Route


def do_routes_shifts_intersect(route_1: Route, route_2: Route) -> bool:
    latest_start = max(route_1.start_time, route_2.start_time)
    earliest_end = min(route_1.end_time, route_2.end_time)
    return latest_start < earliest_end
