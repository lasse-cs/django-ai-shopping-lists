FROM python:3.12-slim-bookworm
RUN apt-get update \
    && apt-get --assume-yes install libpq-dev gcc python3-dev \
    musl-dev zlib1g-dev libjpeg-dev libldap2-dev libsasl2-dev

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock
RUN ["uv", "sync"]

COPY src /src
WORKDIR /src

ENV PORT=8080

CMD uv run manage.py collectstatic --noinput && \
    uv run manage.py migrate && \
    uv run gunicorn config.wsgi:application --bind 0.0.0.0:$PORT 