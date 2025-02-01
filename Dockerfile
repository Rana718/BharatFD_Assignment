# Stage 1
FROM python:3.12-alpine AS builder

WORKDIR /app

RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    postgresql-dev \
    build-base

RUN pip install --no-cache-dir pipenv

COPY Pipfile Pipfile.lock ./

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --ignore-pipfile



# Stage 2
FROM python:3.12-alpine

WORKDIR /app

RUN apk add --no-cache \
    libpq \
    libffi

COPY --from=builder /app/.venv ./.venv

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

RUN adduser -D appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && gunicorn Faq.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
