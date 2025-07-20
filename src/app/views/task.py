from django.db.models import Count, Q
from django.db.models.functions import ExtractWeekDay
from django.utils.timezone import now
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from src.app.models import Task
from src.app.models.task import Status
from src.app.serializers import TaskDetailSerializer


@api_view(['GET'])
def get_all_tasks(request: Request) -> Response:
    query_params = request.query_params
    queryset = Task.objects.all()
    weekday = query_params.get('week_day')

    paginator = PageNumberPagination()
    paginator.page_size = 5
    paginator.page_size_query_param = 'page_size'

    page_size = request.query_params.get('page_size')
    if page_size and page_size.isdigit():
        paginator.page_size = int(page_size)

    if weekday:
        try:
            weekday_int = int(weekday)
            if not 1 <= weekday_int <= 7:
                raise ValueError

            queryset = queryset.annotate(
                weekday=ExtractWeekDay('deadline')
            ).filter(weekday=weekday_int)
        except ValueError:
            return Response({"detail": "weekday must be integer from 1 to 7."}, status=400)

    queryset = queryset.order_by('-created_at')
    paginated_queryset = paginator.paginate_queryset(queryset, request)
    serializer = TaskDetailSerializer(paginated_queryset, many=True)

    return paginator.get_paginated_response(serializer.data)


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
