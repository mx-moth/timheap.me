#!/bin/ash -e

cd /opt/backend

# Run upgrade in the background
./deploy/upgrade.sh &

# Start uwsgi
exec /usr/sbin/uwsgi \
	--ini ./deploy/uwsgi.ini
