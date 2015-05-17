from blog.settings import *
import os


ALLOWED_HOSTS = ['*']
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = False
DEBUG = False  # THIS IS ALSO INDICATES DEVELOPMENT ENVIRONMENT
LANGUAGE_CODE = 'en-us'
MEDIA_URL = '/'
ROOT_URLCONF = 'svenv.urls'
SECRET_KEY = '!k4%c0+yuy2^zu@l_uk2g7h$ya9*m#zfow*0@kv15s0l776%@3'  # NOT FOR PRODUCTION
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = False
STATIC_ROOT = os.path.join('static')
STATIC_URL = '/static/'
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]
TIME_ZONE = 'UTC'
TEMPLATE_DEBUG = DEBUG
USE_I18N = True
USE_L10N = True
USE_TZ = True
WSGI_APPLICATION = 'svenv.wsgi.application'
X_FRAME_OPTIONS = 'DENY'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'blog',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)