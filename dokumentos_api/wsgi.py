import os
import sys
import psycogreen.gevent
import gevent.monkey
from django.core.wsgi import get_wsgi_application

RUNNING_DEVSERVER = (len(sys.argv) > 1 and sys.argv[1] == 'runserver')

if not RUNNING_DEVSERVER:
    gevent.monkey.patch_all()
    psycogreen.gevent.patch_psycopg()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dokumentos_api.settings")

application = get_wsgi_application()
