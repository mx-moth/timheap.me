# Frontend asset builder
FROM node:8-stretch as frontend

ENV NPM_CONFIG_LOGLEVEL=warn

RUN mkdir /app
WORKDIR /app/
COPY package.json yarn.lock /app/

RUN yarn && \
    yarn cache clean && \
    true

COPY ./design/ /app/design/

RUN npm run build
CMD ["npm", "run", "watch"]

# Backend application
FROM alpine as backend

RUN mkdir /app
WORKDIR /app/

RUN apk add --no-cache \
        tini \
        uwsgi uwsgi-python3 \
        python3 python3-dev py3-pillow postgresql-dev gcc musl-dev

RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel

COPY requirements.in requirements.txt /app/
RUN pip3 install --no-cache-dir pyinotify -r requirements.txt

COPY ./timheap /app/timheap
COPY ./deploy /app/deploy
COPY ./manage.py /app/manage.py
COPY --from=frontend /app/static /app/authorsanonymous/static
RUN ln -fs /app/deploy/settings.py /app/settings.py

ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/ \
    DJANGO_SETTINGS_MODULE=settings \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

EXPOSE 80
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["/app/deploy/run.sh"]

FROM backend as tox
RUN pip3 install --no-cache-dir tox
CMD ["tox"]
