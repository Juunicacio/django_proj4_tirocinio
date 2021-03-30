
from django.urls import path
from . import views

urlpatterns = [
    # Thesis stuff, everything after 'localhost/thesis/'
    path('', views.full_thesis, name='full_thesis'),
]
