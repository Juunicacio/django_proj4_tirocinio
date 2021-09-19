#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import django
from data_analysis.scripts.data_analysis.main import *

# run in local
def main():

#if __name__ == '__main__':
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'satellite_telemetry_data_analysis.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

# run in local
if __name__ == '__main__':
    if __name__ == 'daphne satellite_telemetry_data_analysis.asgi:application':
        """
        Before running the application, make sure you had ran the script for data analysis before
        If you had already done that, please ignore this message, and go open your localhost
        """
        main()
    else:
        data_analysis_main()
        print('')
        print("Now, you can run: 'daphne satellite_telemetry_data_analysis.asgi:application' to see the website")
    