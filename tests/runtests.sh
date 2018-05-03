#!/bin/ash

TEST_DATA='/app/test-data'
cd /app
mkdir -p "${TEST_DATA}"

export DJANGO_SETTINGS_MODULE=tests.settings
./manage.py test "$@"
exit_code=$?

rm -rf "${TEST_DATA}"

exit "$exit_code"
