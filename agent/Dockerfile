FROM ghcr.io/astral-sh/uv:python3.11-alpine

WORKDIR /app

COPY . .

RUN uv sync --locked

EXPOSE 8000

CMD ["uv", "run", "poe", "start"]