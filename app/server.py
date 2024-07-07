# from typing import Union

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from api import router
from dotenv import load_dotenv
from asyncio import sleep, create_task

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
        "https://ai-mixologist.vercel.app"
    ]

    app_.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app_


app = create_app()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

async def send_ping(websocket: WebSocket):
    while True:
        try:
            await websocket.send_text("ping")
            await sleep(5)  # Send a ping every 5 seconds
        except Exception:
            break

manager = ConnectionManager()

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    ping_task = create_task(send_ping(websocket))
    try:
        while True:
            await sleep(60)
    except WebSocketDisconnect:
        print("disconnected")
    finally:
        ping_task.cancel()
        manager.disconnect(websocket)
        # await websocket.close()
