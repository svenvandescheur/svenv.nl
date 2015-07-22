from django.core.wsgi import get_wsgi_application
import os


"""
WSGI config for svenv project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "svenv.settings")
application = get_wsgi_application()
