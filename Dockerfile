FROM python:3.12-slim-bookworm AS runtime
ARG UV_VERSION=0.9.7
ARG PROJECT_DIR=/opt/esun
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=Asia/Taipei PYTHONUNBUFFERED=1 LANGSMITH_TRACING=false
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates procps tzdata && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir uv==${UV_VERSION}
WORKDIR ${PROJECT_DIR}
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project --python /usr/local/bin/python
COPY . .
RUN uv sync --frozen --no-dev --python /usr/local/bin/python
ENV PATH="${PROJECT_DIR}/.venv/bin:${PATH}"
CMD ["python", "-m", "esun_research.application"]

FROM runtime AS test
RUN uv sync --frozen --group dev --python /usr/local/bin/python
CMD ["python", "-m", "pytest", "-q"]
