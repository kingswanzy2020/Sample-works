# syntax=docker/dockerfile:1.7
FROM python:3.12-slim AS build
WORKDIR /build
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --prefix=/install -r requirements.txt

FROM python:3.12-slim
ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION} PYTHONUNBUFFERED=1
RUN useradd --uid 10001 --create-home app
WORKDIR /app
COPY --from=build /install /usr/local
COPY src ./src
COPY migrations ./migrations
USER 10001
EXPOSE 8000
# --timeout-graceful-shutdown lets in-flight requests finish on SIGTERM.
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--timeout-graceful-shutdown", "20"]
