from django.urls import path, include
from rest_framework.routers import DefaultRouter

from src.app.views.category import CategoryViewSet

router = DefaultRouter()

router.register(r"categories", CategoryViewSet)

urlpatterns = [
    path('tasks/', include('src.app.urls.task')),
    # path('categories/', include('src.app.urls.category')),
    path('subtasks/', include('src.app.urls.subtask'))
] + router.urls

