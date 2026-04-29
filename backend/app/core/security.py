from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
import bcrypt
from app.core.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.crud.user_crud import user_crud
from app.models.user import User

# 标准 OAuth2（自动报告错误）
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login", auto_error=True)

# 可选 OAuth2（不自动报错，用于公开接口）
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login", auto_error=False)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    user = await user_crud.get(db, id=int(user_id))
    if user is None:
        raise credentials_exception
    return user

# 可选用户（用于公开接口，允许未登录）
async def get_current_user_optional(token: Optional[str] = Depends(oauth2_scheme_optional), db: AsyncSession = Depends(get_db)) -> Optional[User]:
    if not token:
        return None
    try:
        payload = decode_access_token(token)
        if payload is None:
            return None
        user_id = payload.get("sub")
        if user_id is None:
            return None
        user = await user_crud.get(db, id=int(user_id))
        return user
    except:
        return None

class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles
    async def __call__(self, current_user: User = Depends(get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
        return current_user