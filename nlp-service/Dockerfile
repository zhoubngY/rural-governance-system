# 使用 slim 基础镜像（减小体积）
FROM python:3.12-slim

WORKDIR /app

# 设置 pip 国内镜像源（清华源，速度快）
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 复制依赖文件
COPY requirements.txt .

# 安装依赖（如果 torch 下载仍然慢，可考虑使用 CPU 版本）
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY ./app /app/app

# 创建必要目录
RUN mkdir -p /app/data /app/models_store

# 暴露端口
EXPOSE 8001

# 启动命令（根据您的实际入口调整，假设 main.py 在 app 目录下）
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]