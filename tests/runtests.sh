#!/bin/ash

export TEST_DATA=$( mktemp -d )
export DJANGO_SETTINGS_MODULE=tests.settings

cd /opt/backend
./manage.py test "$@"
exit_code=$?

rm -rf "${TEST_DATA}"

exit "$exit_code"
