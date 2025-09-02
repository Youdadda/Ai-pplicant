from fastapi import FastAPI
from routes import base_router, data_router
from helpers.config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient
app = FastAPI()

@app.on_event("startup")
def startup():
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient()
    app.db_client = app.mongo_conn[settings.MONGO_DATABASE]


app.include_router(base_router)
app.include_router(data_router)
