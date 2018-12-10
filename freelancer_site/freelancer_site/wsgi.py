"""
WSGI config for freelancer_site project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
o"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "freelancer_site.settings")

application = get_wsgi_application()


# Update local path in here
path = '/home/abdullah/abdullah/work/projects/freelancer_site/freelancer_site'
if path not in sys.path:
    sys.path.append(path)
