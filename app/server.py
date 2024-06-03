# from typing import Union

from fastapi import FastAPI
from api import router
from dotenv import load_dotenv

from core.config import config

load_dotenv()

def init_routers(app_: FastAPI) -> None:
    app_.include_router(router)

def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Hide",
        description="Hide API",
        version="1.0.0",
        docs_url=None if config.ENV == "production" else "/docs",
        redoc_url=None if config.ENV == "production" else "/redoc",
        # # dependencies=[Depends(Logging)],
        # middleware=make_middleware(),
    )
    init_routers(app_=app_)
    # init_listeners(app_=app_)
    # init_cache()
    return app_


app = create_app()
