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