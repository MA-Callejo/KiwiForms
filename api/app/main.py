import json

from fastapi import FastAPI, WebSocket
from starlette.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocketDisconnect

from app.api.api import api_router
from app.core.config import settings

app = FastAPI( title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json",
              redoc_url=None)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        log_level="debug",
        reload=True,
        workers=1
    )
