"""satellite_telemetry_data_analysis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from dashboard import views
# bring in the functions of the dashGraphs on dash_apps_finished_apps
#from dashboard.dash_apps.finished_apps import TurtleDeepData
from dashboard.dash_apps.finished_apps import simpleExample

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication

    # Dashboard stuff
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard_graphs, name='dashboard_graphs'),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),

    # Thesis stuff
    path('thesis/', include('thesis.urls')),
]
