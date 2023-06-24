from fastapi import FastAPI
from src.controllers import todo
from tortoise.contrib.fastapi import register_tortoise


def get_application():
    setup()
    return create_app()


def create_app() -> FastAPI:
    """
    Create the app and initialize the database.
    """
    from .settings import TORTOISE_ORM

    # https://fastapi.tiangolo.com/tutorial/bigger-applications/?h=apirouter#another-module-with-apirouter
    app = FastAPI()
    register_tortoise(app=app, config=TORTOISE_ORM)

    app.include_router(todo.router, prefix="/api/v1")

    @app.get("/api/v1")
    async def root():
        return {"message": "Hello Bigger Applications!"}

    return app


def setup():
    """
    Load environment variables, validate config and configure logging
    """
    from src.settings import settings

    # configure the logging
    settings.LOGGERS.configure()
