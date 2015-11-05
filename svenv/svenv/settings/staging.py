from base import *


DEBUG = True
MEDIA_URL = 'https://svenv.nl/'
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

INSTALLED_APPS += ('debug_toolbar',)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            '/templates',
        ],
        'OPTIONS': {
            'debug': DEBUG,
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'admin_tools.template_loaders.Loader',
            ],
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]