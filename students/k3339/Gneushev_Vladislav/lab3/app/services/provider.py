from dishka import Provider, provide, Scope

from app.services.assignments import AssignmentService
from app.services.auth import AuthenticationService
from app.services.buses import BusService
from app.services.drivers import DriverService
from app.services.jwt import JWTService
from app.services.routes import RouteService
from app.services.users import UserService


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    get_driver_service = provide(DriverService)
    get_route_service = provide(RouteService)
    get_assignment_service = provide(AssignmentService)
    get_bus_service = provide(BusService)
    get_auth_service = provide(AuthenticationService)
    get_jwt_service = provide(JWTService)
    get_user_service = provide(UserService)
