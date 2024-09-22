FROM python:3.12.3-slim

USER root

RUN mkdir /home/pyuser

WORKDIR /checkbox_api
COPY pyproject.toml poetry.lock* ./


RUN groupadd -g 10001 pyuser && \
   useradd -u 10000 -g pyuser pyuser \
   && chown -R pyuser:pyuser /checkbox_api /home/pyuser /usr/local


USER pyuser:pyuser

RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY . .
EXPOSE 8000

CMD ["uvicorn", "checkbox_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--lifespan", "on", "--reload"]