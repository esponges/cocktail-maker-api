# from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
        debug=True
        # # dependencies=[Depends(Logging)],
        # middleware=make_middleware(),
    )
    init_routers(app_=app_)
    # init_listeners(app_=app_)
    # init_cache()
    origins = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "https://ai-mixologist.vercel.app/"
    ]

    app_.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app_


app = create_app()
