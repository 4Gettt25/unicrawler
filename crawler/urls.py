from django.urls import path
from . import views

urlpatterns = [
    path('download/', views.download_files, name='download_files'),
]