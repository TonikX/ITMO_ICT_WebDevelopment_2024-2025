from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from students.k3341.Lemanov_Andrey.Lr3.app.config.config import config
from students.k3341.Lemanov_Andrey.Lr3.app.api.v1.assigments.assignments_router import assignments_router
from students.k3341.Lemanov_Andrey.Lr3.app.api.v1.grades.grades_router import grade_router
from students.k3341.Lemanov_Andrey.Lr3.app.api.v1.submissions.submissions_router import submission_router
# from students.k3341.Lemanov_Andrey.Lr3.app.api.v1.authentication_router import authentication_router
from students.k3341.Lemanov_Andrey.Lr3.app.config.logger import setup_logging

setup_logging()

app = FastAPI(
    title=config.app.PROJECT_NAME,
    version=config.app.VERSION,
    docs_url=config.app.DOCS_URL,
    openapi_url=config.app.OPENAPI_URL,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.app.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix='/api/v1')


@api_router.get("/healthz")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


api_router.include_router(assignments_router, tags=["Assignments"])
api_router.include_router(grade_router, tags=["Grades"])
api_router.include_router(submission_router, tags=["Submissions"])
# api_router.include_router(authentication_router)
app.include_router(api_router)
