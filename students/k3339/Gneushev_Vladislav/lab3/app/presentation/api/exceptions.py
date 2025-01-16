import logging

from fastapi import FastAPI
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.responses import JSONResponse

from app.services.exceptions import EntityNotFound

logger = logging.getLogger(__name__)


async def validation_exception_handler(request, exc):
    logger.info("Validation error=%s", {"url": request.url, "err": exc})
    return await request_validation_exception_handler(request, exc)


async def entity_not_found_exception_handler(request, exc):
    logger.info("Entity not found error=%s", {"url": request.url, "err": exc})
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(
        exc_class_or_status_code=RequestValidationError,
        handler=validation_exception_handler,
    )
    app.add_exception_handler(
        exc_class_or_status_code=EntityNotFound,
        handler=entity_not_found_exception_handler,
    )
