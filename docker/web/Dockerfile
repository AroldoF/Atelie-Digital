FROM python:3.12-slim

# uv
RUN pip install uv

WORKDIR /app

# dependências python (cache)
COPY pyproject.toml uv.lock /app/

RUN uv sync --no-editable

# projeto
COPY . /app/

EXPOSE 8000

CMD ["sh", "-c", "uv run python manage.py migrate && uv run python manage.py collectstatic --noinput && uv run daphne -b 0.0.0.0 -p 8000 setup.asgi:application"]
