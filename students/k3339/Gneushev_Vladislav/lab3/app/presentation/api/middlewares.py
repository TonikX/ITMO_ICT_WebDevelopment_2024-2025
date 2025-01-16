import logging

from fastapi import Request, Response

logger = logging.getLogger(__name__)


async def access_log_middleware(request: Request, call_next):
    req_status = None
    try:
        response: Response = await call_next(request)
        req_status = response.status_code
        return response
    except Exception:
        req_status = 500
        raise
    finally:
        logger.info("%s %s %s", req_status, request.method, request.url)
