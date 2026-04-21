# 在本地运行（不需要连接数据库）
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed = pwd_context.hash("admin123")  # 替换为你想要的密码
print(hashed)