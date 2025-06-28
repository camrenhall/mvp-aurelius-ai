# app.py
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, create_engine, Session
from config.settings import settings
from controllers.ingest_controller import router as ingest_router
from controllers.callback_controller import router as callback_router

engine = create_engine(settings.database_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

def create_app() -> FastAPI:
    app = FastAPI(title="Aurelius AI MVP")
    
    app.include_router(ingest_router)
    app.include_router(callback_router)
    
    return app

app = create_app()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()