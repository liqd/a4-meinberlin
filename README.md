# Participation Platform mein.berlin

mein.berlin is a participation platform for the city of Berlin, Germany. It is
based on [adhocracy 4](https://github.com/liqd/adhocracy4).

![Build Status](https://github.com/liqd/a4-meinberlin/actions/workflows/django.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/liqd/a4-meinberlin/badge.svg?branch=main)](https://coveralls.io/github/liqd/a4-meinberlin?branch=main)

## Requirements

- Node.js (+ npm)
- Python 3.12 and [uv](https://docs.astral.sh/uv/getting-started/installation/)
- libmagic
- libjpeg
- libpq (only if PostgreSQL is used)
- GDAL
- SpatiaLite [with JSON1 enabled](https://code.djangoproject.com/wiki/JSON1Extension) (only if SpatiaLite is used for local development)
- Redis (required in production, optional for development)

## Installation (Development & Testing Only!)

**Note:** If you are on macOS, you need GNU sed installed for the following steps to work:

```
brew install gnu-sed
```

### Installing SpatiaLite

#### Ubuntu/Debian

```
sudo apt update && sudo apt install -y libsqlite3-mod-spatialite
```

#### macOS (with Homebrew)

```
brew update
brew install spatialite-tools
brew install gdal
```

For GeoDjango to be able to find the SpatiaLite library, add the following to your local.py:

```
SPATIALITE_LIBRARY_PATH = "/usr/local/lib/mod_spatialite.dylib"
```

#### Python version

`pyproject.toml` requires Python 3.12 and `uv sync` uses the interpreter it finds. With pyenv:

```
PYTHON_CONFIGURE_OPTS="--enable-loadable-sqlite-extensions" pyenv install 3.12
# use it for this project's uv commands in this shell; do not export it globally,
# otherwise it may pick another 3.12 without loadable SQLite extensions
export UV_PYTHON="$(pyenv prefix 3.12)/bin/python3"
```

### Steps to Install and Run Development Server

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) first
(`curl -LsSf https://astral.sh/uv/0.13.9/install.sh | sh`; 0.13.x satisfies the
`required-version` in `pyproject.toml`). Dependencies live in `pyproject.toml`
and are locked in `uv.lock`. `make install` installs into `.venv`. Unset any
inherited override first — `deactivate` if another environment is active and
`unset UV_PROJECT_ENVIRONMENT`. Then:

```
git clone https://github.com/liqd/a4-meinberlin.git
cd a4-meinberlin
make install
make fixtures
make watch
```

If you still have a `venv/` directory from the previous pip setup, remove it (`rm -rf venv`);
the environment now lives in `.venv`.

### Start virtual environment

```
source .venv/bin/activate
```

To add a dependency use `uv add <package>`; it updates `pyproject.toml` and `uv.lock`.
adhocracy4 follows the commit locked in `uv.lock` and `package-lock.json`;
`make bump-a4` runs `uv lock --upgrade-package adhocracy4`, `npm update adhocracy4`,
then `scripts/a4-check.sh` to verify both lockfiles agree.
Inside the environment you can also use `uv run python manage.py ...` without activating it.

### Production installation

Build the production environment with only the `prod` extra and no dev group:

```
uv sync --frozen --no-default-groups --extra prod
source .venv/bin/activate
```

Then run `npm install`, `npm run build:prod`, `python manage.py compilemessages`,
`python manage.py collectstatic`. The provided `make release` target runs
`uv sync --locked --no-default-groups --extra prod` for you.

### (Optional) PostgreSQL Database for Testing

If you need to test with PostgreSQL instead of SpatiaLite, run:

```
make postgres-create
```

To start the test server with PostgreSQL:

```
export DATABASE=postgresql
make postgres-start
make watch
```

To remove the Python virtual environment and npm modules:

```
make clean
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

Berlin.de base styles for the public site are vendored as `meinberlin/assets/berlin_css/berlin_marketing.scss` (from `berlin.de/i9f/r1/bundle/berlin_marketing.css`) and imported via `style_user_facing.scss`.

For style-guide alignment with the **Vertical Participation** design system ([designsystem.berlin.de](https://designsystem.berlin.de/latest/bundle/berlin_participation.css)), we **merge in only the relevant rules and tokens** via meinBerlin SCSS overrides — we do **not** replace the marketing bundle wholesale.

**Merged from participation (via overrides):**

| Change | Override location |
|--------|-------------------|
| Primary green `#439c76` (`$primary`, `$panel-colored`) | `styles_user_facing/variables/_colors.scss` |
| `.panel--colored` background | `components_user_facing/_service-panel.scss` |
| `.text--color-primary` | `styles_user_facing/_utility.scss` |
| Search submit arrow colour | `components_user_facing/_searchform-slot.scss` |
| Topic pills (`pill--topic`) | `components_user_facing/_pill.scss` |

**meinBerlin-only layout fixes** (not in either vendor bundle): teaser blocks, hero, accordion, content footer — see `components_user_facing/` and `changelog/style-guide-alignment.md`.

**Updating vendor CSS (before releases):**

- Download `berlin_marketing.css` from berlin.de; update paths in `berlin_marketing.scss` as noted in the file header.
- When the participation style guide changes, diff `berlin_participation.css` against marketing and port only what meinBerlin still needs into the override files above.
- Run `npm run build` and regression-test key pages.

Font Awesome and `berlin_marketing.js` are still loaded from berlin.de separately (`base.html`). Until upstream versions are pinned, update vendor CSS only before releases — breaking changes are not always announced.
