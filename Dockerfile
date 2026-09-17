# syntax=docker/dockerfile:1

FROM node:22-bookworm-slim AS assets

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# husky installs git hooks and would fail because the build context has no .git.
ENV HUSKY=0

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build:prod


FROM python:3.12-bookworm AS app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=meinberlin.config.settings.docker

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gdal-bin \
        libgdal-dev \
        libgeos-dev \
        libproj-dev \
        libpq-dev \
        gettext \
        postgresql-client \
        git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements requirements
RUN pip install --no-cache-dir -r requirements/dev.txt

COPY . .
COPY --from=assets /app/meinberlin/static /app/meinberlin/static

# Collect static files so the WSGI server (granian) can serve them via
# WhiteNoise; the dev server (runserver) is not used in containers.
RUN python manage.py collectstatic --noinput

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8003

ENTRYPOINT ["/entrypoint.sh"]
CMD ["granian", "--interface", "wsgi", "--host", "0.0.0.0", "--port", "8003", "--log-level", "warning", "meinberlin.config.wsgi:application"]
