FROM ghcr.io/astral-sh/uv:python3.14-rc-bookworm-slim
ADD . /app
WORKDIR /app
RUN uv sync --frozen --no-cache
EXPOSE 8000
CMD ["/app/.venv/bin/uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--reload"]
