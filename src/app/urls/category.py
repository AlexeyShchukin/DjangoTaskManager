from django.urls import path

from src.app.views import create_category, update_category

urlpatterns = [
    path('create/', create_category),
    path('update/', update_category)
]