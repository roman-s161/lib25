# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u2625143/data/www/librarytgn.ru/pythonProject1/libraryProject')
sys.path.insert(1, '/var/www/u2625143/data/env/lib/python3.10/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'libraryProject.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
