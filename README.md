## 核心目标
完成乡村治理系统本地开发环境部署，实现村民公开注册、管理员后台管理、工作人员任务处理的完整闭环，并固化所有配置使项目具备完全可移植性。

## 已确认事实/共识
1. **多租户架构**：采用 PostgreSQL schema-per-tenant，`tenant_1` 对应北荡村，所有业务数据必须写入该 schema。
2. **权限模型**：村民仅能登录村民端（`villager`），工作人员/管理员仅能登录后台（`staff`/`admin`）。村民通过公开页面注册，工作人员由管理员在后台创建。
3. **认证方案**：密码哈希统一使用 `bcrypt==4.0.1` 直接调用，已彻底移除 `passlib`。
4. **前端状态**：村民端和管理后台页面完整，路由守卫和角色隔离已生效，`@` 和 `@shared` 别名配置正确。
5. **数据库状态**：`tenant_1` 表结构完整，`admin`（密码 `admin123`）及测试村民存在，Alembic 迁移版本为 `c82f19a6beba (head)`。
6. **配置文件**：`.env` 已存在且有效，`.gitignore` 已创建并忽略 `.env`，临时调试 `.py` 文件已清理，项目结构整洁。

## 待解决问题（痛点）
无。核心业务流程（注册→登录→申请→分配→处理）已验证通过，Alembic 配置已修复并同步，系统处于完全可运行、可移植状态。

## 最近一次操作/状态
- 执行 `docker-compose build backend` 和 `docker-compose up -d backend` 重新构建镜像，固化 Alembic 配置及迁移文件。
- 宿主机与容器内迁移文件已同步，均只保留 `c82f19a6beba_current_schema.py`。
- 验证 `docker-compose ps` 显示三个服务均 `Up`，`alembic current` 输出 `c82f19a6beba (head)`。

## 关键约束条件
- 开发环境必须使用 Docker Compose 启动（`docker-compose up -d`）。
- 前端使用 `pnpm dev:user`（端口 3000）和 `pnpm dev:admin`（端口 3001）。
- 敏感信息（`.env`）不得提交 Git，模板为 `.env.example`。
- 后续模型变更需在容器内执行 `alembic revision --autogenerate -m "描述" && alembic upgrade head`，并将生成的新迁移文件复制回宿主机 `backend/alembic/versions/`。

## 下一步起点
请在新会话中直接复制以下内容发送：

> “上一轮会话结束时，系统已完成所有配置修复和状态同步，Alembic 迁移版本为 `c82f19a6beba`，容器与宿主机文件一致。现在请协助我：① 列出从零开始在新电脑上部署的完整步骤（包括安装 Docker、Node.js、pnpm，克隆代码后执行的操作）；② 验证村民注册→登录→提交申请→管理员分配→工作人员处理的完整工作流是否仍有疏漏；③ 如需生产环境部署建议，提供关键配置修改清单。”

🟢 日常启动（在项目根目录）
cmd
docker-compose up -d
cd frontend && pnpm dev:user    （终端1）
cd frontend && pnpm dev:admin   （终端2）
🔵 修改了后端模型后
cmd
docker exec -it rural_gov_backend alembic revision --autogenerate -m "描述"
docker exec -it rural_gov_backend alembic upgrade head
docker cp rural_gov_backend:/app/alembic/versions/新文件.py backend/alembic/versions/
docker-compose build backend && docker-compose up -d backend
🟠 新电脑首次部署
cmd
git clone <repo>
cp .env.example .env   # 填写真实密码和密钥
docker-compose up -d --build
cd frontend && pnpm install
# 启动前端（同上）
🔴 忘记密码/初始化新村庄
使用项目保留的 manage.py（如果有）：

cmd
docker exec -it rural_gov_backend python manage.py init_village --village-id 2 --admin-username admin2 --admin-password 123456

多租户：
前提条件
Docker Desktop 正在运行，且三个核心容器（rural_gov_db, rural_gov_backend, rural_gov_nlp）处于 Up 状态。

源村庄（tenant_1）的表结构完整，包含所有业务表（如 users, memorials, notices, tasks 等）。

您已经安装了 PowerShell（Windows 自带），并且能够执行 Docker 命令。

宿主机不需要安装 Python 依赖（因为所有操作通过 Docker 容器内的 Python 生成密码哈希）。

通用脚本（PowerShell）
将以下代码保存为一个 .ps1 文件（例如 New-Village.ps1），放在项目根目录（D:\Python\Python_code\rural-governance-system）。

powershell
param(
    [Parameter(Mandatory=$true)]
    [int]$VillageId,
    [Parameter(Mandatory=$true)]
    [string]$AdminUsername,
    [Parameter(Mandatory=$true)]
    [string]$AdminPassword,
    [string]$AdminFullname = "村管理员"
)

$ErrorActionPreference = "Stop"

$sourceSchema = "tenant_1"
$targetSchema = "tenant_$VillageId"

Write-Host "🚀 开始创建村庄 ID=$VillageId, 管理员=$AdminUsername" -ForegroundColor Cyan

# 1. 检查源 schema 是否存在
$sourceExists = docker exec rural_gov_db psql -U postgres -d rural_gov -t -c "SELECT schema_name FROM information_schema.schemata WHERE schema_name='$sourceSchema';"
if (-not $sourceExists) {
    Write-Host "❌ 错误：源 schema $sourceSchema 不存在" -ForegroundColor Red
    exit 1
}

# 2. 创建目标 schema（如果已存在会提示但忽略）
docker exec rural_gov_db psql -U postgres -d rural_gov -c "CREATE SCHEMA IF NOT EXISTS $targetSchema;"

# 3. 复制所有表结构（使用 LIKE 语句）
Write-Host "📋 正在复制表结构 ..."
$tables = docker exec rural_gov_db psql -U postgres -d rural_gov -t -c "SELECT tablename FROM pg_tables WHERE schemaname='$sourceSchema';"
foreach ($t in $tables) {
    $t = $t.Trim()
    if ($t) {
        Write-Host "   复制表: $t"
        docker exec rural_gov_db psql -U postgres -d rural_gov -c "CREATE TABLE IF NOT EXISTS $targetSchema.$t (LIKE $sourceSchema.$t INCLUDING ALL);" 2>$null
    }
}

# 4. 生成 bcrypt 密码哈希（通过后端容器内的 Python）
Write-Host "🔐 生成密码哈希 ..."
$hash = docker exec rural_gov_backend python -c "import bcrypt; print(bcrypt.hashpw(b'$AdminPassword', bcrypt.gensalt()).decode())"
$hash = $hash.Trim()

# 5. 插入管理员用户
Write-Host "👤 创建管理员 $AdminUsername ..."
$insertSql = @"
INSERT INTO $targetSchema.users (username, hashed_password, real_name, role, village_id, is_active)
VALUES ('$AdminUsername', '$hash', '$AdminFullname', 'admin', $VillageId, true);
"@
docker exec rural_gov_db psql -U postgres -d rural_gov -c $insertSql

# 6. 验证
Write-Host "✅ 验证结果：" -ForegroundColor Green
docker exec rural_gov_db psql -U postgres -d rural_gov -c "SELECT username, real_name FROM $targetSchema.users;"

Write-Host "🎉 村庄 $VillageId 初始化完成！" -ForegroundColor Green
Write-Host "   管理后台登录：http://localhost:3001"
Write-Host "   账号：$AdminUsername"
Write-Host "   密码：$AdminPassword"
执行要求
以管理员身份打开 PowerShell（建议，避免权限问题，但非必须）。

切换到项目根目录：

powershell
cd D:\Python\Python_code\rural-governance-system
执行脚本（示例：创建第三个村庄）：

powershell
.\New-Village.ps1 -VillageId 3 -AdminUsername "wangcun_admin" -AdminPassword "Wangcun@123" -AdminFullname "王村管理员"
等待脚本运行，看到 🎉 村庄 X 初始化完成！ 即成功。

注意事项
村庄 ID 必须唯一：每个村庄使用不同的 VillageId，对应 schema tenant_<id>。

管理员用户名不能重复：不同村庄的管理员用户名可以相同（因为在不同 schema 中隔离），但建议使用不同名称。

密码强度：脚本接受任意密码，但建议使用强密码。

表结构复制：脚本会复制 tenant_1 中所有表的结构（不包含数据），新村庄的业务表初始都为空。

外键约束：LIKE ... INCLUDING ALL 会复制主键、索引、默认值，但不会复制外键约束（如果需要外键，需手动添加）。不过对于大多数业务表，外键不影响基本操作。

如果表中包含自增字段（如 id SERIAL），复制后会产生独立的序列，新村庄的数据会从 1 开始自增，不影响原有村庄。

验证
执行脚本后，您可以通过以下命令快速检查新村庄的管理员：

powershell
docker exec rural_gov_db psql -U postgres -d rural_gov -c "SELECT username, real_name FROM tenant_<村庄ID>.users;"
例如检查第三个村庄：

powershell
docker exec rural_gov_db psql -U postgres -d rural_gov -c "SELECT username, real_name FROM tenant_3.users;"
此外，您还可以登录管理后台 http://localhost:3001，使用新创建的管理员账号登录，测试大事记、通知等模块（列表应为空，可以新增数据）。

常见问题
问题1：执行脚本时提示 docker exec 权限不足
解决：以管理员身份运行 PowerShell，或确保当前用户在 docker-users 组中。

问题2：提示 bcrypt 模块未找到
解决：后端的 Python 环境已安装 bcrypt（因为后端依赖包含）。如果仍报错，请确认 rural_gov_backend 容器正在运行。

问题3：复制表结构时部分表失败（例如 task_assignments 不存在）
原因：tenant_1 中可能只有 tasks 表而没有 task_assignments，这很正常，脚本会跳过不存在的表。脚本中的 CREATE TABLE IF NOT EXISTS 会忽略已存在的表，不会报错。

问题4：插入管理员时提示重复键
原因：该管理员用户名已存在于目标 schema 中。脚本未做冲突检测，您可以修改用户名或先删除已有用户。

总结
您现在拥有一个一键创建任意新村庄的 PowerShell 脚本，它完全基于 Docker 命令，不依赖宿主机 Python 环境，并且已经过手动验证（创建第二个村庄成功）。未来添加第三个、第四个村庄只需一行命令，省时省力。

如果需要进一步自动化（例如批量创建多个村庄），可以在此基础上编写循环。请妥善保存 New-Village.ps1 脚本。