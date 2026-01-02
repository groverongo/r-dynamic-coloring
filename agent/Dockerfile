FROM ghcr.io/astral-sh/uv:python3.11-alpine

WORKDIR /app

ENV UV_NO_DEV=1
ENV HOST=0.0.0.0
ENV PORT=8000

ENV PYTHONPATH=$PYTHONPATH:/app/src

COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock
COPY .python-version .python-version

RUN uv sync --locked

COPY src src

EXPOSE 8000

CMD [ "uv", "run", "uvicorn", "src:app", "--host", "0.0.0.0", "--port", "8000" ]