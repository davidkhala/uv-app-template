FROM python:slim

WORKDIR /app

RUN pip install uv

COPY . .

# 把依赖直接装进容器的 系统环境（即镜像里的全局 Python 环境）
RUN uv pip install --system . 

CMD uv run uvicorn main:app --host 0.0.0.0 --port $PORT
