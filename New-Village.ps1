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