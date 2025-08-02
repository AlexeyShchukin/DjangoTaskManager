from django.urls import path

from src.app.views import get_statistic
from src.app.views.task import TaskListCreateView, TaskRetrieveUpdateDestroyView, MyTasksListView

urlpatterns = [
    path('', TaskListCreateView.as_view()),
    path('statistic/', get_statistic),
    path('my_tasks/', MyTasksListView.as_view(), name='My tasks'),
    path('<int:task_id>/', TaskRetrieveUpdateDestroyView.as_view()),
]