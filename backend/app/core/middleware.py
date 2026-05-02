from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.database import tenant_schema_var
from app.core.security import decode_access_token
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        public_paths = [
            "/",
            "/docs",
            "/redoc",
            "/openapi.json",
            f"{settings.API_V1_STR}/auth/login",
            f"{settings.API_V1_STR}/users/register",
            f"{settings.API_V1_STR}/openapi.json",
            f"{settings.API_V1_STR}/memorials",
            f"{settings.API_V1_STR}/notices",
            f"{settings.API_V1_STR}/guides",
            f"{settings.API_V1_STR}/notes",
            f"{settings.API_V1_STR}/policies",
        ]

        # 匹配逻辑：路径完全相同 或 以路径+斜杠开头
        for p in public_paths:
            if request.url.path == p or request.url.path.startswith(p + "/"):
                logger.debug(f"Public path matched: {request.url.path}")
                return await call_next(request)

        logger.debug(f"Path {request.url.path} not in public, checking tenant...")
        tenant_id = request.headers.get("X-Tenant-ID")
        if not tenant_id:
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
                payload = decode_access_token(token)
                if payload:
                    tenant_id = payload.get("tenant_id")
        if not tenant_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tenant ID not found")

        tenant_schema = f"tenant_{tenant_id}"
        token = tenant_schema_var.set(tenant_schema)
        request.state.tenant_id = tenant_id
        try:
            response = await call_next(request)
        finally:
            tenant_schema_var.reset(token)
        return response