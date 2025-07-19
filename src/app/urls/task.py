from django.urls import path

from src.app.views import get_all_tasks, create_task, get_statistic, get_task_by_id

urlpatterns = [
    path('', get_all_tasks),
    path('create/', create_task),
    path('statistic/', get_statistic),
    path('<int:task_id>/', get_task_by_id),
]