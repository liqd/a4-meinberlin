#!/bin/sh
set -e

# Run migrations
python manage.py migrate -v0

# Then the given command
exec "$@"
