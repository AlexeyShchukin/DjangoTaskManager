from django.urls import path

from src.app.views.subtask import SubTaskListCreateView, SubTaskDetailUpdateDeleteView

urlpatterns = [
    path('', SubTaskListCreateView.as_view()),
    path('<int:pk>', SubTaskDetailUpdateDeleteView.as_view()),
]
