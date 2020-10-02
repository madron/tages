#!/bin/bash
set -e

if [ "$1" = 'uwsgi' ]; then
    echo 'Wait for database'
    gosu nobody python3 /src/manage.py wait_for_database
    echo 'Migrate'
    gosu nobody python3 /src/manage.py migrate --noinput
    ARGS="$*"
    echo "gosu nobody uwsgi ${ARGS:6}"
    exec gosu nobody uwsgi ${ARGS:6}
elif [ "$1" = 'celery' ] && [ "$2" = 'flower' ]; then
    chown nobody /data
    echo "$@"
    exec gosu nobody "$@"
elif [ "$1" = 'celery' ]; then
    if [ "$2" = 'flower' ]; then
        chown nobody /data
    fi
    echo 'Wait for database'
    gosu nobody python3 /src/manage.py wait_for_database
    echo "$@"
    exec gosu nobody "$@"
elif [ "$1" = 'nginx' ]; then
    exec nginx "-g daemon off;"
else
    exec "$@"
fi
