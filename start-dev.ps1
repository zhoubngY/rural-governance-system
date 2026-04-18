Write-Host "========================================" -ForegroundColor Green
Write-Host "  启动乡村治理系统开发环境" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

Write-Host "[1/3] 启动 Docker 容器..." -ForegroundColor Yellow
docker-compose up -d

Write-Host "[2/3] 等待后端就绪..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host "[3/3] 启动前端服务（将打开新窗口）..." -ForegroundColor Yellow
Start-Process cmd -ArgumentList "/k cd /d $PWD\frontend\packages\web-user && npx vite --port 3000"
Start-Process cmd -ArgumentList "/k cd /d $PWD\frontend\packages\web-admin && npx vite --port 3001"

Write-Host "========================================" -ForegroundColor Green
Write-Host "  启动完成！" -ForegroundColor Green
Write-Host "  村民端: http://localhost:3000" -ForegroundColor Cyan
Write-Host "  管理后台: http://localhost:3001" -ForegroundColor Cyan
Write-Host "  后端文档: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Green
Read-Host "按 Enter 键退出"