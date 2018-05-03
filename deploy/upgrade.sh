#!/bin/ash -e

./manage.py migrate --noinput
./manage.py collectstatic --noinput
