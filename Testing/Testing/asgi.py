"""
ASGI config for Testing project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Testing.settings')
django.setup()

#application = get_asgi_application()
application = ProtocolTypeRouter({
    "http" : AsgiHandler(),
})