FROM python:3.10.21-slim-trixie AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml uv.lock ./
COPY src/ ./src/
RUN uv build --wheel --out-dir /app/dist

## Etapa 2
FROM python:3.10.21-slim-trixie AS runner
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app

#Instalamos uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
ENV PATH="/app/.venv/bin:$PATH"

#Copiamos el wheel
COPY --from=builder /app/dist /tmp/dist

#Instalamos el wheel
RUN uv pip install /tmp/dist/*.whl && rm -rf /tmp/dist

#Descargamos el modelo
RUN hf download Felisuco092/timeSeriesSalesKaggle model.joblib --repo-type model --local-dir /app/models

#Copiamos el código
COPY api/ ./api/

#Exponemos el puerto
EXPOSE 8000

CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8000"]