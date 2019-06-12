import os
import sys

sys.path.append('/var/www/jhela')
sys.path.append('/usr/local/lib/python2.7/site-packages/django')
os.environ['DJANGO_SETTINGS_MODULE'] = 'jhela.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()
