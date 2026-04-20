# 改动说明：
# • 新增 DATABASE_URL 可选环境变量，优先使用。
# • 提供 async_database_url 属性（供 FastAPI 使用），自动添加 SSL 并处理驱动。
# • 提供 sync_database_url 属性（供 Alembic 使用），自动转换为同步驱动。
# • 保留原有的 POSTGRES_* 变量作为本地开发的回退方案。
from pydantic_settings import BaseSettings
from typing import List, Optional
from pydantic import AnyHttpUrl, validator
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "乡村治理系统"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "CHANGE_ME_TO_A_VERY_SECURE_RANDOM_STRING_32_CHARS"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # CORS 配置：支持从环境变量注入多个域名，逗号分隔
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:5173"
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        return v

    # 数据库配置：优先使用 DATABASE_URL 环境变量（生产），否则使用下面的参数构建
    DATABASE_URL: Optional[str] = None

    # 本地开发参数（仅当 DATABASE_URL 为空时使用）
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "rural_gov"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    @property
    def sync_database_url(self) -> str:
        """同步驱动 URL（用于 Alembic 等）"""
        if self.DATABASE_URL:
            # 将 asyncpg 替换为 psycopg2 或保持原样，但 Alembic 需要同步驱动
            return self.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://").split("?")[0]
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

    @property
    def async_database_url(self) -> str:
        """异步驱动 URL（用于 FastAPI）"""
        if self.DATABASE_URL:
            url = self.DATABASE_URL
            # 确保使用 asyncpg 驱动
            if "postgresql+asyncpg" not in url:
                url = url.replace("postgresql://", "postgresql+asyncpg://")
            # 为 Supabase 添加 SSL 要求
            if "supabase" in url and "sslmode" not in url:
                url += "?sslmode=require"
            return url
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

    # 租户 schema 配置（保留原有逻辑）
    PUBLIC_SCHEMA_NAME: str = "public"

    # NLP 服务地址
    NLP_SERVICE_URL: str = "http://localhost:8001"

    # 文件上传限制
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024
    UPLOAD_DIR: str = "./uploads"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()