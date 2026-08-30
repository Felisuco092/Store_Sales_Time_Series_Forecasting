FROM python:3.10.21-slim-trixie AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app

# Desactiva la caché persistente para no inflar capas
ENV UV_NO_CACHE=1 \
    UV_COMPILE_BYTECODE=1

COPY pyproject.toml uv.lock ./
COPY src/ ./src/

# Creamos el entorno virtual, instalamos dependencias y el propio paquete
RUN uv sync --frozen --no-dev --no-editable

#Descargamos el modelo
RUN uv run hf download Felisuco092/timeSeriesSalesKaggle model.joblib --repo-type model --local-dir /app/models

#Descargamos la dependencia src del proyecto
RUN uv pip install .

## Etapa 2
FROM python:3.10.21-slim-trixie AS runner

WORKDIR /app

# Copiamos exclusivamente el entorno virtual y el modelo ya listos
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/models /app/models

#El entorno virtual en el PATH
ENV PATH="/app/.venv/bin:$PATH"

#Copiamos el código y el pyproject.toml
COPY pyproject.toml ./
COPY api/ ./api/

#Exponemos el puerto
EXPOSE 8000

CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8000"]