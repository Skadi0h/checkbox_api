FROM python:3.12.3-slim

WORKDIR /checkbox_api
COPY pyproject.toml poetry.lock* ./

RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

COPY . .
EXPOSE 8000

CMD ["uvicorn", "checkbox_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--lifespan", "on", "--reload"]