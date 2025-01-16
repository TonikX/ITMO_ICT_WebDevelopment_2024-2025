from fastapi import FastAPI, APIRouter

from .drivers import router as drivers_router
from .routes import router as routes_router
from .buses import router as buses_router
from .assignments import router as assignments_router
from .auth import router as auth_router


def register_routes(app: FastAPI):
    router = APIRouter(prefix='/api')
    router.include_router(drivers_router)
    router.include_router(routes_router)
    router.include_router(buses_router)
    router.include_router(assignments_router)
    router.include_router(auth_router)

    app.include_router(router)
