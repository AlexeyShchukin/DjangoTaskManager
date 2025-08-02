from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from src.app.views.category import CategoryViewSet

router = DefaultRouter()

router.register(r"categories", CategoryViewSet)

urlpatterns = [
    path('tokens/', TokenObtainPairView.as_view()),
    path('tokens/refresh/', TokenRefreshView.as_view()),
    path('tasks/', include('src.app.urls.task')),
    # path('categories/', include('src.app.urls.category')),
    path('subtasks/', include('src.app.urls.subtask'))
] + router.urls

