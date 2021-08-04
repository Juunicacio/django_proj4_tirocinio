"""
WSGI config for satellite_telemetry_data_analysis project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
#from data_analysis.scripts.data_analysis import main

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'satellite_telemetry_data_analysis.settings')
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'from data_analysis.scripts.data_analysis.main.setting')

application = get_wsgi_application()
