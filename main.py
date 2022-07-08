from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT

from app.todo import models
from app.todo.api.v1 import router
from app.user.api.v1 import user_router, denylist

from core.config import settings
from db.database import engine

models.Base.metadata.create_all(bind=engine)


@AuthJWT.load_config
def get_config():
    return settings


@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in denylist


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()

app.include_router(user_router)
app.include_router(router, prefix="/api/v1")


