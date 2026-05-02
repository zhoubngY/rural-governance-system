from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
import logging
from app.core.database import get_db, tenant_schema_var
from app.core.security import create_access_token, verify_password
from app.crud.user_crud import user_crud
from app.schemas.token import Token
from app.core.config import settings
from app.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

@router.post("/login", response_model=Token)
async def login(db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    tenant_schema_var.set("tenant_1")
    await db.execute(text('SET search_path TO tenant_1'))
    user = await user_crud.get_by_username(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token(
        data={"sub": str(user.id), "tenant_id": user.village_id, "role": user.role},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    # 临时绕过认证：直接返回 id=1 的 admin 用户
    tenant_schema_var.set("tenant_1")
    await db.execute(text('SET search_path TO tenant_1'))
    result = await db.execute(select(User).where(User.id == 1))
    user = result.scalar_one_or_none()
    if user:
        return user
    # 如果数据库中无 id=1 的用户，则回退到原有逻辑（但一般都有）
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # ... 原有代码（保留作为备用，但不会执行到）
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    tenant_schema_var.set("tenant_1")
    await db.execute(text('SET search_path TO tenant_1'))
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user

async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in ["admin", "staff"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user