# syntax=docker/dockerfile:1

# The image is built in three stages so that build-only tooling (Node/npm,
# compilers, -dev headers, gettext) never ends up in the runtime layer:
#
#   assets       -> node + npm, only the compiled JS/CSS is copied over
#   python-deps  -> slim python + compilers/headers, only the venv is copied
#   app          -> slim python + runtime libs + venv + source
#
# The former single-stage build used the full python:3.12-bookworm image and
# kept gdal/geos/proj development headers, git, gettext and the whole dev
# dependency set in the deployed image, which dominated the image size.

# Both Python stages must use the same image: the venv is built in one stage
# and copied into the other, and it references the interpreter and bytecode of
# that exact Python build.
ARG PYTHON_IMAGE=python:3.12-slim-bookworm

# --- 1. Frontend assets ------------------------------------------------------

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


# --- 2. Python dependencies --------------------------------------------------

FROM ${PYTHON_IMAGE} AS python-deps

ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Compilers and headers are only needed when a wheel has to be built from
# source (psycopg[c] from requirements/prod.txt, any package without a wheel).
# This stage is discarded, so they never inflate the runtime image.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        git \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN python -m venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY requirements requirements
# The prod requirements instead of the dev set: the image only needs to run
# the app, not the test/lint tooling.
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements/prod.txt


# --- 3. Runtime --------------------------------------------------------------

FROM ${PYTHON_IMAGE} AS app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=meinberlin.config.settings.docker \
    PATH="/app/.venv/bin:$PATH"

# Runtime libraries only:
#   gdal-bin            GeoDjango, ogr2ogr (import_geodata), pulls libgdal32/
#                       libgeos/libproj/proj-data
#   libgeos-c1v5        explicit GEOS runtime for django.contrib.gis
#   libmagic1           python-magic (requirements/bplan serializers)
#   libpq5, libstdc++6  psycopg[c] / bundled native extensions
#   postgresql-client   pg_isready in the entrypoint
# The -dev variants from the old single-stage build are gone.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gdal-bin \
        libgeos-c1v5 \
        libmagic1 \
        libpq5 \
        libstdc++6 \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY --from=python-deps /app/.venv /app/.venv

WORKDIR /app

COPY . .
COPY --from=assets /app/meinberlin/static /app/meinberlin/static

# gettext is only needed for compilemessages. Installing, compiling and
# purging it in a single RUN keeps it out of the resulting layer.
RUN apt-get update \
    && apt-get install -y --no-install-recommends gettext \
    && python manage.py compilemessages -v0 \
    && python manage.py collectstatic --noinput \
    && apt-get purge -y --auto-remove gettext \
    && rm -rf /var/lib/apt/lists/*

COPY --chmod=755 docker/entrypoint.sh /entrypoint.sh

EXPOSE 8003

ENTRYPOINT ["/entrypoint.sh"]
CMD ["granian", "--interface", "wsgi", "--host", "0.0.0.0", "--port", "8003", "--log-level", "warning", "meinberlin.config.wsgi:application"]
