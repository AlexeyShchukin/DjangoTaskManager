from django.urls import path, include

urlpatterns = [
    path('tasks/', include('src.app.urls.task')),
    path('categories/', include('src.app.urls.category')),
    path('subtasks/', include('src.app.urls.subtask'))
]