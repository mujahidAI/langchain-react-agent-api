FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./

# --no-install-project skips installing the local project during dependency sync
RUN uv sync --frozen --no-dev --no-install-project

COPY . .

# Now install the project itself after all files are copied
RUN uv sync --frozen --no-dev

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]