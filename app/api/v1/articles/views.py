from fastapi import APIRouter, Depends

articles_router = APIRouter(prefix="/api/v1/articles", tags=["Articles"])
