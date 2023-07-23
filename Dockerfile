# 使用Python的官方镜像作为基础镜像
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 复制/src目录到/app目录下
COPY src /app

# 安装项目依赖项
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# 暴露容器内的端口，设置为80
EXPOSE 80

# 启动FastAPI应用程序并绑定到80端口
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]