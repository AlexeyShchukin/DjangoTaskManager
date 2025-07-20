from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from src.app.models import SubTask
from src.app.serializers import SubTaskCreateSerializer, SubTaskSerializer


class SubTaskListCreateView(APIView):
    def get(self, request: Request) -> Response:
        query_params = request.query_params
        queryset = SubTask.objects.all()
        task_title = query_params.get('task')
        subtask_status =query_params.get('status')

        if task_title:
            queryset = queryset.filter(task__title=task_title)

        if subtask_status:
            queryset = queryset.filter(status=subtask_status)

        serializer = SubTaskSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailUpdateDeleteView(APIView):
    def get_object(self, pk: int) -> SubTask:
        return get_object_or_404(SubTask, pk=pk)

    def get(self, request: Request, pk: int) -> Response:
        subtask = self.get_object(pk=pk)
        serializer = SubTaskSerializer(subtask)
        return Response(serializer.data)

    def put(self, request: Request, pk: int) -> Response:
        subtask = self.get_object(pk)
        serializer = SubTaskSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int) -> Response:
        subtask = self.get_object(pk)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
