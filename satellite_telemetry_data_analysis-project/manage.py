#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import django
from data_analysis.scripts.data_analysis.main import *


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

# run on server
if __name__ == '__main__':
    if __name__ == 'python3 manage.py runserver' or __name__ == 'py manage.py runserver':
        data_analysis_main()
        print('')
        print("Now, you can run: 'daphne satellite_telemetry_data_analysis.asgi:application' to see the website")

    if __name__ == 'daphne satellite_telemetry_data_analysis.asgi:application':
        """
        Before running the application, make sure you had ran the script for data analysis before
        If you had already done that, please ignore this message, and go open your localhost
        """
        main()
# run in local
# if __name__ == '__main__':
#     if __name__ == 'daphne satellite_telemetry_data_analysis.asgi:application':
#         """
#         Before running the application, make sure you had ran the script for data analysis before
#         If you had already done that, please ignore this message, and go open your localhost
#         """
#         main()
#     else:
#         data_analysis_main()
#         print('')
#         print("Now, you can run: 'daphne satellite_telemetry_data_analysis.asgi:application' to see the website")
    