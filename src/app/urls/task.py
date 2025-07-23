from django.urls import path

from src.app.views import get_statistic
from src.app.views.task import TaskListCreateView, TaskRetrieveUpdateDestroyView

urlpatterns = [
    path('', TaskListCreateView.as_view()),
    path('<int:task_id>/', TaskRetrieveUpdateDestroyView.as_view()),
]