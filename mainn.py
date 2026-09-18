from database import engine, Base
from fastapi import FastAPI
from routers.auth import router as auth_router
from routers.luxury import router as luxury_router

app = FastAPI(title="AMG Cyber Luxury Store API",
              description="Коммерческий API с поддержкой Redis, JWT, PostgreSQL и внешних интеграций через httpx",
              version="1.0.0")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth_router)
app.include_router(luxury_router)

@app.get("/")
async def home():
    return {"message": "Сервер работает, архитектура на  роутерах готова"}



