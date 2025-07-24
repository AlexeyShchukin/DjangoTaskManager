from typing import Any
from datetime import datetime, timezone

from rest_framework import serializers

from src.app.models import Task, SubTask
from src.app.models.category import Category


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'


class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True)

    class Meta:
        model = Task
        fields = '__all__'


class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = '__all__'


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

        def validate_deadline(self, value):
            if value < datetime.now():
                raise serializers.ValidationError("Deadline can not be in the past")
            return value


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data: dict[str, Any]):
        name = validated_data["name"]

        if Category.objects.filter(name=name).exists():
            raise serializers.ValidationError("Category with this name is already exists.")

        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data: dict[str, Any]):
        if Category.objects.exclude(id=instance.id).filter(name=validated_data["name"]).exists():
            raise serializers.ValidationError({"name": "Category with this name already exists."})

        return super().update(instance, validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
