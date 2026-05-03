import asyncio
import argparse
import subprocess
import sys

async def run_sql(sql: str):
    """通过 docker exec 执行 SQL"""
    cmd = f'docker exec -i rural_gov_db psql -U postgres -d rural_gov -c "{sql}"'
    proc = await asyncio.create_subprocess_shell(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        print(f"SQL error: {stderr.decode()}")
        return False
    print(stdout.decode())
    return True

async def schema_exists(schema_name: str) -> bool:
    """检查 schema 是否存在"""
    cmd = f'docker exec rural_gov_db psql -U postgres -d rural_gov -t -c "SELECT schema_name FROM information_schema.schemata WHERE schema_name = \'{schema_name}\'"'
    proc = await asyncio.create_subprocess_shell(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, _ = await proc.communicate()
    return bool(stdout.decode().strip())

async def copy_schema(source_schema: str, target_schema: str):
    """复制表结构（使用 CREATE TABLE LIKE）"""
    # 获取源 schema 中的所有表名
    cmd = f'docker exec rural_gov_db psql -U postgres -d rural_gov -t -c "SELECT tablename FROM pg_tables WHERE schemaname = \'{source_schema}\'"'
    proc = await asyncio.create_subprocess_shell(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, _ = await proc.communicate()
    tables = [t.strip() for t in stdout.decode().splitlines() if t.strip()]
    for table in tables:
        # 创建目标表（复制结构，不包含数据）
        sql = f'CREATE TABLE IF NOT EXISTS {target_schema}.{table} (LIKE {source_schema}.{table} INCLUDING ALL)'
        if not await run_sql(sql):
            print(f"复制表 {table} 失败")
            return False
        # 可选：复制索引、约束等（LIKE INCLUDING ALL 已经包含）
    print(f"✅ 从 {source_schema} 复制表结构到 {target_schema} 完成")
    return True

async def init_village(village_id: int, admin_username: str, admin_password: str, admin_fullname: str):
    target_schema = f"tenant_{village_id}"
    source_schema = "tenant_1"

    # 1. 检查源 schema 是否存在
    if not await schema_exists(source_schema):
        print(f"错误：源 schema {source_schema} 不存在")
        return

    # 2. 创建目标 schema
    if await schema_exists(target_schema):
        print(f"Schema {target_schema} 已存在，跳过复制")
    else:
        if not await run_sql(f'CREATE SCHEMA "{target_schema}"'):
            return
        if not await copy_schema(source_schema, target_schema):
            return

    # 3. 生成密码哈希（使用 bcrypt）
    # 通过 Python 生成哈希（不依赖后端模块）
    import bcrypt
    hashed = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode()

    # 4. 插入管理员用户
    insert_sql = f"""
    INSERT INTO {target_schema}.users (username, hashed_password, real_name, role, village_id, is_active)
    VALUES ('{admin_username}', '{hashed}', '{admin_fullname}', 'admin', {village_id}, true)
    ON CONFLICT (username) DO NOTHING;
    """
    if await run_sql(insert_sql):
        print(f"✅ 村庄 {village_id} 初始化完成")
        print(f"   管理员账号：{admin_username} / {admin_password}")
    else:
        print("插入管理员失败")

async def main():
    parser = argparse.ArgumentParser(description="乡村治理系统管理工具")
    subparsers = parser.add_subparsers(dest="command", required=True)
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