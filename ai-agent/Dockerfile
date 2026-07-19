FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml ./

RUN pip install --no-cache-dir uv

COPY . .

RUN uv sync

EXPOSE 8000

CMD ["uv", "run", "python", "app.py"]