import sys
RUNNING_DEVSERVER = (len(sys.argv) > 1 and sys.argv[1] == 'runserver')

if not RUNNING_DEVSERVER:
	import gevent.monkey
	gevent.monkey.patch_all()
	import psycogreen.gevent
	psycogreen.gevent.patch_psycopg()

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dokumentos_api.settings")

application = get_wsgi_application()
