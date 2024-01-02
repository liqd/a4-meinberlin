# Participation platform mein.berlin

mein.berlin is a participation platform for the city of Berlin, Germany. It is
based on [adhocracy 4](https://github.com/liqd/adhocracy4).

![Build Status](https://github.com/liqd/a4-meinberlin/actions/workflows/django.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/liqd/a4-meinberlin/badge.svg?branch=main)](https://coveralls.io/github/liqd/a4-meinberlin?branch=main)

## Requirements

- nodejs (+ npm)
- python 3.x (+ venv + pip)
- libmagic
- libjpeg
- libpq (only if postgres should be used)
- gdal
- sqlite3 [with JSON1 enabled](https://code.djangoproject.com/wiki/JSON1Extension)(only if sqlite is used for local development)
- redis (in production, not needed for development)

## Installation (for development and testing only!)
Note: if you are on a mac you need to have gnu sed installed for the following
steps to work. Install it via brew:
```
brew install gnu-sed
```
Steps to install and run a development server:
```
git clone https://github.com/liqd/a4-meinberlin.git
cd a4-meinberlin
make install
make fixtures
make watch
````

### (Optional) postgresql database for testing:
If you need to do testing with postgresql as database (usually sqlite is
sufficient).

run the following command once:

```
make postgres-create
```

to start the testserver with postgresql, run:

```
export DATABASE=postgresql
make postgres-start
make watch
```

### (Optional) celery for task queues
If you need to do testing with a proper celery setup.

For celery to register and run tasks you need to make sure that:

- the redis server is running
- the celery config parameter "always eager" is disabled (add `CELERY_TASK_ALWAYS_EAGER = False` to your `local.py`)

To start a celery worker in the foreground, run:

```
make celery-worker-start
```
Stop celery with ctr+C

To inspect all registered tasks, list the running worker nodes, run:

```
make celery-worker-status
```

To send a dummy task to the queue and report the result, run:

```
make celery-worker-dummy-task
```

See more info about Celery in the [docs](./docs/celery.md)

### (Optional) celery beat for scheduled tasks in development
If you need to do testing with periodical task working.

For celery to run scheduled tasks you need to make sure that:

- the redis server is running
- the celery worker is running (see previous step)

To start celery beat in the foreground, run:

```
make celery-beat
```
Stop celery beat with ctr+C

### To add scheduled tasks (same for all environments) check the [docs](./docs/celerybeat.md)

In case of settings.TIME_ZONE change, tasks need to be synced with the new time. [See HOWTO](https://django-celery-beat.readthedocs.io/en/latest/#important-warning-about-time-zones)

### Style Library

-   currently all js and css incl fontawesome files are downloaded due to difficulties serving files and slowing development
    -   img and font resouce paths within the berlin css have been updated to include the local version
-   Until versioning of libraries implemented prefered solution would be to have js downloaded once per day and cached, css should only be updated before release due to issues of breaking changes not being versioned or announced.
