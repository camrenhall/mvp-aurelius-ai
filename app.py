# app.py
from fastapi import Depends, FastAPI
from sqlmodel import Session, SQLModel, create_engine

from config.settings import settings

engine = create_engine(settings.database_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def create_app() -> FastAPI:
    app = FastAPI(title="Aurelius AI MVP")

    # Import routers here to avoid circular imports
    from controllers.callback_controller import router as callback_router
    from controllers.ingest_controller import router as ingest_router

    app.include_router(ingest_router)
    app.include_router(callback_router)

    return app


app = create_app()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
