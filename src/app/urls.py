from django.urls import path

from src.app.views import get_all_tasks, create_task, get_statistic, get_task_by_id

urlpatterns = [
    path('tasks/', get_all_tasks),
    path('tasks/create/', create_task),
    path('tasks/statistic', get_statistic),
    path('tasks/<int:task_id>/', get_task_by_id)
]