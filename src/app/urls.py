from django.urls import path

from src.app.views import hello

urlpatterns = [
    path('', hello)
]