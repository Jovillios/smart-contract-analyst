FROM python:3.13-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-cache 

COPY src ./src

ENV PYTHONPATH=/app
ENV PATH="/app/.venv/bin:$PATH"