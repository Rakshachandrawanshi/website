"""
WSGI config for company project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'company.settings')

application = get_wsgi_application()

if os.environ.get("RENDER") and os.environ.get("DJANGO_AUTO_MIGRATE", "True").lower() in ("1", "true", "yes", "on"):
    call_command("migrate", interactive=False, verbosity=1)
