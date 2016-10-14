"""
WSGI config for base project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""
import os,sys


sys.path.append('/home/daret/fbasicas/dj_basicas')
sys.path.append('/home/daret/fbasicas/1.10.1/lib/python2.7/site-packages/')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")


application = get_wsgi_application()