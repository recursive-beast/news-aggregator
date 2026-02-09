FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir pipenv watchdog

COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

COPY . .

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser
