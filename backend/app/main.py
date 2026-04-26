# 改动说明：
# 未作实质改动，只是确认了导入和中间件顺序。如果你原来的 main.py 有其他内容（如静态文件挂载等），请合并进去。
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, users, tasks, notes, policy
from app.core.middleware import TenantMiddleware
from app.core.database import engine
from app.models.base import Base

async def init_db():
    async with engine.begin() as conn:
        # 生产环境建议使用 Alembic 迁移，这里仅作为本地开发快速建表
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

# CORS 中间件 —— 必须放在最前面
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 租户中间件
app.add_middleware(TenantMiddleware)

# 注册路由
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)
app.include_router(tasks.router, prefix=settings.API_V1_STR)
app.include_router(notes.router, prefix=settings.API_V1_STR)
app.include_router(policy.router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/")
async def root():
    return {"message": "乡村治理系统 API"}
#Reloading...