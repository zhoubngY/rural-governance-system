# manage.py
# 村庄初始化命令行工具
# 使用方法:cmd运行 python manage.py init_village --village-id 2 --admin-username admin_cun2 --admin-password Cun2@123 --admin-fullname "李庄村管理员"
# manage.py 是一个宿主机执行的 Python 脚本，用于在已运行的后端容器内创建新村庄的独立数据库 schema 和初始管理员账号。它不是在容器内运行的。
# 🚀 具体使用方法
# 1️⃣ 确保后端容器正在运行
# cmd
# docker-compose up -d backend
# 2️⃣ 在项目根目录执行命令（CMD 或 PowerShell）
# 初始化第一个村庄（北荡村，village_id=1）
# cmd
# python manage.py init_village --village-id 1 --admin-username admin --admin-password admin123 --admin-fullname "北荡村管理员"
# 初始化第二个村庄（例如李庄村，village_id=2）
# cmd
# python manage.py init_village --village-id 2 --admin-username lizhuang_admin --admin-password Lizhuang@123 --admin-fullname "李庄村管理员"
# ⚙️ 参数说明
# 参数	必填	说明
# --village-id	✅	村庄唯一数字 ID，将用于创建 schema tenant_{id}
# --admin-username	✅	该村初始管理员的登录用户名
# --admin-password	✅	初始管理员密码
# --admin-fullname	❌	管理员显示姓名，默认为“村管理员”
# 🧩 底层发生了什么？
# 脚本通过 SQLAlchemy 连接到运行中的数据库容器（使用 .env 中的连接信息）。
# 执行 CREATE SCHEMA IF NOT EXISTS tenant_{village_id}。
# 在该 schema 内执行 Base.metadata.create_all() 创建所有业务表（与 tenant_1 结构完全一致）。
# 在 tenant_{village_id}.users 表中插入管理员记录，密码用 bcrypt 哈希。
# 结果：新村庄拥有完全独立的数据库空间，与其他村庄数据物理隔离。
# 📌 重要提醒
# 每次新增村庄，必须分配一个全新的、未被使用过的 village_id。
# 该命令不会影响现有村庄，可随时安全执行。
# 若需为已有村庄补充管理员，可直接通过后台用户管理界面创建，或连接数据库手动插入。
# ✅ 验证新村庄是否成功
# cmd
# docker exec -it rural_gov_db psql -U postgres -d rural_gov -c "SET search_path TO tenant_2; SELECT username FROM users;"
import asyncio
import argparse
from sqlalchemy import text
from app.core.database import AsyncSessionLocal, engine
from app.models.base import Base
from app.crud.user_crud import user_crud
from app.core.security import get_password_hash

async def create_tenant_schema(village_id: int):
    """创建租户 schema 并在其中建表"""
    schema_name = f"tenant_{village_id}"
    async with engine.begin() as conn:
        await conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema_name}"'))
        await conn.execute(text(f'SET search_path TO "{schema_name}"'))
        await conn.run_sync(Base.metadata.create_all)
    print(f"✅ 村庄 {village_id} 的数据库 schema 已创建")

async def init_village(village_id: int, admin_username: str, admin_password: str, admin_fullname: str):
    """初始化村庄：创建 schema + 初始管理员"""
    # 1. 创建租户 schema
    await create_tenant_schema(village_id)
    
    # 2. 在租户 schema 中创建管理员
    async with AsyncSessionLocal() as db:
        await db.execute(text(f'SET search_path TO "tenant_{village_id}"'))
        existing = await user_crud.get_by_username(db, username=admin_username)
        if existing:
            print(f"⚠️ 管理员 {admin_username} 已存在，跳过创建")
            return
        user_data = {
            "username": admin_username,
            "hashed_password": get_password_hash(admin_password),
            "full_name": admin_fullname,
            "role": "admin",
            "village_id": village_id,
        }
        await user_crud.create(db, obj_in=user_data)
        await db.commit()
        print(f"✅ 村庄 {village_id} 初始化完成")
        print(f"   管理员账号：{admin_username} / {admin_password}")

async def main():
    parser = argparse.ArgumentParser(description="乡村治理系统管理工具")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 子命令: init_village
    init_parser = subparsers.add_parser("init_village", help="初始化一个新村庄")
    init_parser.add_argument("--village-id", type=int, required=True, help="村庄唯一ID")
    init_parser.add_argument("--admin-username", required=True, help="初始管理员用户名")
    init_parser.add_argument("--admin-password", required=True, help="初始管理员密码")
    init_parser.add_argument("--admin-fullname", default="村管理员", help="管理员姓名")

    args = parser.parse_args()
    if args.command == "init_village":
        await init_village(args.village_id, args.admin_username, args.admin_password, args.admin_fullname)

if __name__ == "__main__":
    asyncio.run(main())