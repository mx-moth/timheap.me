#!/bin/ash

TEST_DATA='/app/test-data'
cd /app
mkdir -p "${TEST_DATA}"

./manage.py test "$@"

rm -rf "${TEST_DATA}"
