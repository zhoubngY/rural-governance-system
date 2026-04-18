from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from sqlalchemy import select

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_username(self, db, *, username: str):
        result = await db.execute(select(self.model).where(self.model.username == username))
        return result.scalars().first()

user_crud = CRUDUser(User)
