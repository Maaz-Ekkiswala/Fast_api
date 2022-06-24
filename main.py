from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.todo import models
from app.todo.api.v1 import router

from core.config import settings
from db.database import engine

models.Base.metadata.create_all(bind=engine)


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()

app.include_router(router, prefix="/api/v1")
