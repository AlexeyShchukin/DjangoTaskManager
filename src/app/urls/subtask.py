from django.urls import path

from src.app.views.subtask import SubTaskListCreateView, SubTaskRetrieveUpdateDestroyView

urlpatterns = [
    path('', SubTaskListCreateView.as_view()),
    path('<int:subtask_id>', SubTaskRetrieveUpdateDestroyView.as_view()),
]
