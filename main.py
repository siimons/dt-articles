import uvicorn
from fastapi import FastAPI
from app.api.v1.views import router


def create_application() -> FastAPI:
    app = FastAPI(
        title="Dev Talk API",
        description="RESTful API for managing articles",
        version="1.0.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )
    app.include_router(router, prefix="/api/v1", tags=["Articles"])
    return app


app = create_application()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        log_level="info",
        reload=True
    )
