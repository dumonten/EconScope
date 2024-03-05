"""
ASGI config for econ_scope project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'econ_scope.settings')
djangp_asgi_app = get_asgi_application()


application = ProtocolTypeRouter({
    "http": djangp_asgi_app,
})
