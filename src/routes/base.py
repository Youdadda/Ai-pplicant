from fastapi import APIRouter
from fastapi.responses import JSONResponse

base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"]
)

@base_router.get("/")
async def welcome():
    return JSONResponse(
        content={
            "message":"Welcome to the Self-RAG app"
        }
    )