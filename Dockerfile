FROM ghcr.io/astral-sh/uv:python3.14-rc-bookworm-slim
ARG MARKDOWN_COLLECTION_REPO_URL
ARG MARKDOWN_COLLECTION_DIR
ADD . /app
WORKDIR /app
# Pull markdown collection
RUN apt-get update && apt-get install -y git
RUN git clone ${MARKDOWN_COLLECTION_REPO_URL} ${MARKDOWN_COLLECTION_DIR}
RUN uv sync --frozen --no-cache
EXPOSE 8000
CMD ["/app/.venv/bin/uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--reload"]
