from base import *


EXCLUDE_FROM_MINIFYING = ('^sitemap.xml',)
X_FRAME_OPTIONS = 'ALLOW'
pw = open('/pw.txt').read().splitlines()[0]
SECRET_KEY = pw
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'svenv.nl',
        'USER': 'svenv.nl',
        'PASSWORD': 'my-secret-password',
        'HOST': 'postgresql',
    }
}
