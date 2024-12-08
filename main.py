from fastapi import FastAPI
import uvicorn

from app.api.router import router

def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(router)
    return application

app = get_application()

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, log_level="info")