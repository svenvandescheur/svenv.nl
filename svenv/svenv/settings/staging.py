from base import *


DEBUG = True
MEDIA_URL = 'http://svenv.nl/'
TEMPLATE_DEBUG = True
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