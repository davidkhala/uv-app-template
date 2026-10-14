FROM python:slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app

COPY . .

# 把依赖直接装进容器的 系统环境（即镜像里的全局 Python 环境）
RUN uv pip install --system --no-cache . 

EXPOSE $PORT

CMD uv run uvicorn main:app --host 0.0.0.0 --port $PORT
