import uvicorn
from fastapi import FastAPI

from app.api.v1.articles.views import router as articles_router
from app.api.v1.tags.views import router as tags_router
from app.core.dependencies.common import lifespan


def create_application() -> FastAPI:
    app = FastAPI(
        title="Dev Talk API - Articles",
        description="RESTful API for managing articles",
        version="1.0.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        lifespan=lifespan,
    )

    app.include_router(articles_router)
    app.include_router(tags_router)

    return app


app = create_application()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True
    )
