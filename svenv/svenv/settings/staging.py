from base import *


EXCLUDE_FROM_MINIFYING = ('^sitemap.xml',)
X_FRAME_OPTIONS = 'ALLOW'
key = open('/srv/uwsgi/key.txt').read().splitlines()[0]
pw = open('/srv/uwsgi/pw.txt').read().splitlines()[0]
SECRET_KEY = key
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'svenv.nl',
        'USER': 'svenv.nl',
        'PASSWORD': pw,
        'HOST': 'postgresql',
    }
}
