#!/bin/bash
set -e

function print_help {
    echo "mein.berlin Docker development tools"
    echo
    echo "Usage:"
    echo "  ./docker-make.sh install         -- Install dependencies and setup project"
    echo "  ./docker-make.sh build           -- Build the Docker images"
    echo "  ./docker-make.sh up              -- Start all containers"
    echo "  ./docker-make.sh down            -- Stop all containers"
    echo "  ./docker-make.sh fixtures        -- Load all fixtures"
    echo "  ./docker-make.sh test            -- Run all tests"
    echo "  ./docker-make.sh pytest          -- Run Python tests"
    echo "  ./docker-make.sh jstest          -- Run JS tests"
    echo "  ./docker-make.sh lint            -- Run linters"
    echo "  ./docker-make.sh shell           -- Open a shell in the web container"
    echo "  ./docker-make.sh manage [cmd]    -- Run Django manage.py commands"
    echo "  ./docker-make.sh npm [cmd]       -- Run npm commands"
    echo "  ./docker-make.sh clean           -- Remove containers and volumes"
    echo
}

case "$1" in
    install)
        docker-compose build
        docker-compose run --rm web python manage.py migrate
        docker-compose run --rm web python manage.py collectstatic --noinput
        ;;
    build)
        docker-compose build
        ;;
    up)
        docker-compose up
        ;;
    down)
        docker-compose down
        ;;
    fixtures)
        docker-compose run --rm web /usr/local/bin/docker-fixtures.sh
        ;;
    test)
        docker-compose run --rm web py.test --reuse-db
        docker-compose run --rm node npm run testNoCov
        ;;
    pytest)
        docker-compose run --rm web py.test --reuse-db
        ;;
    jstest)
        docker-compose run --rm node npm run test
        ;;
    lint)
        docker-compose run --rm web isort --diff -c meinberlin tests
        docker-compose run --rm web flake8 meinberlin tests --exclude migrations,settings
        docker-compose run --rm node npm run lint
        docker-compose run --rm web python manage.py makemigrations --dry-run --check --noinput
        ;;
    shell)
        docker-compose run --rm web bash
        ;;
    manage)
        shift
        docker-compose run --rm web python manage.py "$@"
        ;;
    npm)
        shift
        docker-compose run --rm node npm "$@"
        ;;
    clean)
        docker-compose down -v
        ;;
    *)
        print_help
        ;;
esac