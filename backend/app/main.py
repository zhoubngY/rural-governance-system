from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, users, tasks, notes, policy
from app.core.middleware import TenantMiddleware
from app.core.database import engine
from app.models.base import Base
from pathlib import Path

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TenantMiddleware)

app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)
app.include_router(tasks.router, prefix=settings.API_V1_STR)
app.include_router(notes.router, prefix=settings.API_V1_STR)
app.include_router(policy.router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    await init_db()
    uploads_dir = Path("/app/uploads/tasks")
    uploads_dir.mkdir(parents=True, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "乡村治理系统 API"}