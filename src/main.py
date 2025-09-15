from fastapi import FastAPI
from routes import base_router, data_router
from helpers.config import get_settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.llm.templates.template_parser import TemplateParser
from contextlib import asynccontextmanager




@asynccontextmanager
async def lifespan(app:FastAPI):
    settings = get_settings()
    postrges_conn = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}/{settings.POSTGRES_MAIN_DATABASE}"
    app.db_engine = create_async_engine(postrges_conn)
    app.db_client = sessionmaker(
        app.db_engine, class_ = AsyncSession, expire_on_commit=False,
    )

    llm_provider_factory = LLMProviderFactory(settings)
    
    app.process_client = llm_provider_factory.create(provider=settings.GENERATION_PROVIDER)
    app.process_client.set_generation_model(model_id=settings.GENERATION_MODEL)

    app.template_parser = TemplateParser(
        language=settings.PRIMARY_LANG,
        default_language=settings.DEFAULT_LANG
    )
    yield
    
    
    await app.db_engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(data_router)
app.include_router(base_router)

