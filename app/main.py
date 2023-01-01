from fastapi import FastAPI, Request, Response, HTTPException

from starlette.requests import Request
from starlette.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from app.config.config import settings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.routes.router import router
from app.models.user_model import User
from app.models.document_model import Document

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def index():
    return {"message": "Server is Working, go to /docs to test apis"}


@app.on_event("startup")
async def server_initialization():

    db = AsyncIOMotorClient(settings.MONGO_URI).smallconvertertools

    await init_beanie(
        database=db,
        document_models=[
            User,
            Document
        ]
    )
    print("database connected")


app.include_router(router, prefix=settings.API)
