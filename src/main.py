import uvicorn
from fastapi import APIRouter
from fastapi import FastAPI

from src.sender.routes import sender_router
from src.settings import project_settings

app = FastAPI(title=project_settings.APP_TITLE)


main_router = APIRouter(prefix=project_settings.API_URL_PREFIX)
main_router.include_router(sender_router)
app.include_router(main_router)


if __name__ == "__main__":
    uvicorn.run(app=app, host=project_settings.APP_HOST, port=project_settings.APP_PORT)
