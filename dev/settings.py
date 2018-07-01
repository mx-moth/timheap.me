from dj_database_url import parse

from timheap.settings import *  # noqa
from timheap.settings import INSTALLED_APPS

INSTALLED_APPS = INSTALLED_APPS + [
    'wagtail.contrib.styleguide',
]

SECRET_KEY = 'super secret shhhhh'
DEBUG = True

ALLOWED_HOSTS = ['timheap.vcap.me', '*', 'localhost']
INTERNAL_IPS = ['127.0.0.1', '172.19.0.1']
BASE_URL = 'http://timheap.vcap.me'

DATA_ROOT = '/opt/data/'

DATABASES = {
    'default': parse('postgres://postgres@database/postgres'),
}

MEDIA_ROOT = DATA_ROOT + 'media/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail'
EMAIL_PORT = 25
