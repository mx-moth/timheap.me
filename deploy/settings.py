import os

from dj_database_url import parse
from timheap.settings import *  # noqa

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
DEBUG = bool(int(os.environ['DJANGO_DEBUG']))

HOSTNAME = os.environ['DJANGO_HOSTNAME']
PROTOCOL = os.environ['DJANGO_PROTOCOL']

ALLOWED_HOSTS = [HOSTNAME]
BASE_URL = '{}://{}'.format(PROTOCOL, HOSTNAME)

DEFAULT_FILE_STORAGE = 'timheap.storage.S3MediaStorage'
STATICFILES_STORAGE = 'timheap.storage.S3StaticStorage'

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_AUTO_CREATE_BUCKET = True
AWS_QUERYSTRING_AUTH = False

DATABASES = {
    'default': parse(os.environ['DATABASE_URL']),
}

EMAIL_BACKEND = 'django_ses.SESBackend'
SERVER_EMAIL = DEFAULT_FROM_EMAIL = os.environ['DJANGO_FROM_EMAIL']

WAGTAIL_SITE_NAME = "Tim Heap"

ADMINS = ['errors@timheap.me']
