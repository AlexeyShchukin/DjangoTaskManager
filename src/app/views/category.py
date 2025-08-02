from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication

from src.app.models.category import Category
from src.app.serializers import CategoryCreateSerializer, CategorySerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.prefetch_related("tasks")
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    @action(methods=["get"], detail=False, url_path="tasks_count")
    def count_tasks(self, request):
        count_tasks = self.queryset.values("id").annotate(
            task_count=Count("tasks")
        )
        return Response(
            data=count_tasks,
            status = status.HTTP_200_OK
        )

# @api_view(['POST'])
# def create_category(request: Request) -> Response:
#     raw_data = request.data
#
#     serializer = CategoryCreateSerializer(data=raw_data)
#
#     if serializer.is_valid():
#         serializer.save()
#         return Response(data=serializer.data, status=status.HTTP_200_OK)
#
#     return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['PUT'])
# def update_category(request: Request, category_id: int) -> Response:
#     category = get_object_or_404(Category, id=category_id)
#     raw_data = request.data
#     serializer = CategoryCreateSerializer(instance=category, data=raw_data)
#
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
