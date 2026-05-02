from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, users, tasks, notes, policy
from app.api.v1 import memorials, notices, guides, applications, consultations  # 新增
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
    allow_origins=["*"],
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
# 新增路由
app.include_router(memorials.router, prefix=settings.API_V1_STR)
app.include_router(notices.router, prefix=settings.API_V1_STR)
app.include_router(guides.router, prefix=settings.API_V1_STR)
app.include_router(applications.router, prefix=settings.API_V1_STR)
app.include_router(consultations.router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    await init_db()
    uploads_dir = Path("/app/uploads/tasks")
    uploads_dir.mkdir(parents=True, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "乡村治理系统 API"}