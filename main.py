import uvicorn
from fastapi import FastAPI
from src.router import app


def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(app)
    return application

app = get_application()

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000, log_level='debug')