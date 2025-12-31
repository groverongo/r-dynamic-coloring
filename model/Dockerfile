FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0

ENV UV_NO_DEV=1

RUN apk add --no-cache glpk

COPY .python-version .python-version
COPY pyproject.toml pyproject.toml 
COPY uv.lock uv.lock

RUN uv sync --locked

COPY main main

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
