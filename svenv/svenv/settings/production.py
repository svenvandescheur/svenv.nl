from base import *


EXCLUDE_FROM_MINIFYING = ('^sitemap.xml',)
X_FRAME_OPTIONS = 'ALLOW'
random = open('/random.txt').read().splitlines()[0]
SECRET_KEY = random
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'svenv_nl',
        'USER': 'admin',
        'PASSWORD': random,
        'HOST': 'localhost',
        'PORT': '3306',
    }
}