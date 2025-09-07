from fastapi import FastAPI
from routes import base_router, data_router
from helpers.config import get_settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

app = FastAPI()

@app.on_event("startup")
def startup():
    settings = get_settings()
    settings = get_settings()
    postrges_conn = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}/{settings.POSTGRES_MAIN_DATABASE}"
    
    app.db_engine = create_async_engine(postrges_conn)
    app.db_client = sessionmaker(
        app.db_engine, class_ = AsyncSession, expire_on_commit=False,
    )


app.include_router(base_router)
app.include_router(data_router)
