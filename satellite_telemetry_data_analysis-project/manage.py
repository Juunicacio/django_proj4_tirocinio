#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import django
#from data_analysis.scripts.data_analysis.main import *


def main():
    #run_main_of_data_analysis()
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

#def run_main_of_data_analysis():
    #os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.setting')
    #django.setup()
    # now your code can go here...
    # Call here the function data_analysis_main() inside main.py of data_analysis app
    #data_analysis_main()


if __name__ == '__main__':
    main()