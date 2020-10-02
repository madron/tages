#!/bin/sh
set -e

coverage run --rcfile=.coveragerc-mt manage.py test mastergest
coverage html
coverage report --skip-covered
