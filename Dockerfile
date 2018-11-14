# Frontend asset builder
FROM node:8-stretch as frontend

ENV NPM_CONFIG_LOGLEVEL=warn

WORKDIR /opt/frontend
COPY package.json yarn.lock /opt/frontend/

RUN yarn && \
	yarn cache clean && \
	true

COPY ./design/ /opt/frontend/design/

RUN yarn run build
CMD ["yarn", "run", "watch"]

# Backend application
FROM alpine as backend

WORKDIR /opt/backend

RUN apk add --no-cache \
		tini \
		python3 python3-dev py3-pillow \
		postgresql-dev gcc musl-dev \
		uwsgi uwsgi-python3 \
	&& true

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel \
	&& pip3 install --no-cache-dir pyinotify -r /tmp/requirements.txt \
	&& rm /tmp/requirements.txt \
	&& true

COPY ./timheap /opt/backend/timheap
COPY ./deploy /opt/backend/deploy
COPY ./manage.py /opt/backend/manage.py
COPY --from=frontend /opt/frontend/static /opt/frontend/static

ENV PYTHONUNBUFFERED=1 \
	PYTHONIOENCODING=UTF-8 \
	PYTHONDONTWRITEBYTECODE=1 \
	DJANGO_SETTINGS_MODULE=deploy.settings \
	LC_ALL=C.UTF-8 \
	LANG=C.UTF-8 \
	UWSGI_PROCESSES=1

EXPOSE 80
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["/opt/backend/deploy/run.sh"]
