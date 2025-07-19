from django.db.models import Count, Q
from django.utils.timezone import now
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from src.app.models import Task
from src.app.models.task import Status
from src.app.serializers import TaskDetailSerializer


@api_view(['GET'])
def get_all_tasks(request: Request) -> Response:
    response_data = Task.objects.all()
    serializer = TaskDetailSerializer(data=response_data, many=True)
    if serializer.is_valid():
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_task_by_id(request: Request, task_id: int) -> Response:
    task = get_object_or_404(Task, id=task_id)
    serializer = TaskDetailSerializer(task)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_task(request: Request) -> Response:
    raw_data = request.data

    serializer = TaskDetailSerializer(data=raw_data)

    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_statistic(request: Request) -> Response:
    total_tasks = Task.objects.count()

    tasks_by_status = Task.objects.values('status').annotate(count_by_status=Count('id'))

    overdue_tasks = Task.objects.filter(
        ~Q(status=Status.DONE),
        deadline__lt=now()
    ).count()

    response_data = {
        'total_tasks': total_tasks,
        'tasks_by_status': {obj['status']: obj['count_by_status'] for obj in tasks_by_status},
        'overdue_tasks': overdue_tasks
    }

    return Response(data=response_data, status=status.HTTP_200_OK)
