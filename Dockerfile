# Build Variables
ARG APP_ROOT=/srv
ARG DJANGO_BUILD_SETTINGS_MODULES=meinberlin.config.settings.build

# Runtime Variables (may be overwritten by env)
ARG DJANGO_SETTINGS_MODULE=meinberlin.config.settings.production
ARG WSGI_APP=meinberlin.config.whitenoise

FROM python:3.6-alpine3.6 AS build

ARG APP_ROOT
ARG DJANGO_BUILD_SETTINGS_MODULES

ENV DJANGO_SETTINGS_MODULE=${DJANGO_BUILD_SETTINGS_MODULES} \
    PATH=${APP_ROOT}/bin:${PATH}

# Install additional required libraries
RUN apk add --no-cache \
  build-base \
  git \
  nodejs-npm \
  postgresql-dev \
  zlib-dev \
  libffi-dev \
  libxml2-dev \
  libxslt-dev \
  jpeg-dev \
  libmagic \
  gettext

WORKDIR ${APP_ROOT}
COPY . ${APP_ROOT}

# Install npm and build webpack
RUN npm install --no-save && \
    npm run build && \
    rm -rf node_modules

# Install python dependencies
RUN python -m venv ${APP_ROOT} && \
    pip install --no-cache-dir -r requirements.txt

# Initialize Django
RUN python manage.py collectstatic --noinput -v0 && \
    python manage.py compilemessages -v0



FROM python:3.6-alpine3.6

ARG APP_ROOT
ARG DJANGO_SETTINGS_MODULE
ARG WSGI_APP

ENV DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE} \
    WSGI_APP=${WSGI_APP} \
    PATH=${APP_ROOT}/bin:${PATH}

WORKDIR ${APP_ROOT}
COPY --from=build ${APP_ROOT} ${APP_ROOT}

# PIL: libz libjpeg
# Brotli: libstdc++ libgcc
# lxml: libz libxslt libxml libgcrypt libz libgpg
# cffi: libffi
# psycopg: libpq libcrypto libldap liblber libsasl

RUN apk add --no-cache \
  libpq \
  zlib \
  libffi \
  libxml2 \
  libxslt \
  libjpeg \
  libmagic \
  libstdc++

EXPOSE 6000
ENTRYPOINT ["scripts/run_after_migrations.sh", \
            "gunicorn", \
              "--env", "DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}", \
              "--bind", "0.0.0.0:6000", \
              "--workers", "2", \
              "${WSGI_APP}"]
