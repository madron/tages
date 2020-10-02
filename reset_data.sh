#!/usr/bin/env sh

rm -rf db.sqlite3
./manage.py migrate --noinput --verbosity=1
