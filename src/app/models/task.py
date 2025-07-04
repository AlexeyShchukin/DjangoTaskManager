from datetime import datetime
from enum import StrEnum

from django.db import models
from django.db.models import ForeignKey, UniqueConstraint, F
from django.db.models.functions import TruncDate


class Status(StrEnum):
    NEW = "New"
    IN_PROGRESS = "In Progress"
    PENDING = "Pending"
    BLOCKED = "Blocked"
    DONE = "Done"

    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]


class Task(models.Model):
    """
   Represents a main task with a title, description,
   categories, status, and deadline.
   """
    title: str = models.CharField(
        max_length=100
    )
    description: str = models.TextField(
        null=True,
        blank=True
    )
    categories = models.ManyToManyField(
        'Category',
        symmetrical=False,
        related_name='tasks',
    )

    status: str = models.CharField(
        choices=Status.choices(),
        default="New",
    )
    deadline: datetime = models.DateTimeField(
        null=True,
        blank=True
    )
    created_at: datetime = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )

    class Meta:
        """Meta options for the Task model."""
        db_table = "'task_manager_task'"
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ["-created_at"]
        constraints = [
            UniqueConstraint(
                F('title'),
                TruncDate('created_at'),
                name='unique_task_title_per_day',
                violation_error_message="A task with this title already exists for this date."
            )
        ]

    def __str__(self):
        """String representation of the Task object."""
        return self.title


class SubTask(models.Model):
    title: str = models.CharField(
        max_length=100,
        unique=True
    )
    description: str = models.TextField(
        null=True,
        blank=True
    )

    task = ForeignKey(
        'Task',
        on_delete=models.CASCADE,
        related_name='subtasks',
        verbose_name="Parent Task"
    )
    status: str = models.CharField(
        choices=Status.choices(),
        default="New",
    )
    deadline: datetime = models.DateTimeField(
        null=True,
        blank=True
    )
    created_at: datetime = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )

    class Meta:
        """Meta options for the SubTask model."""
        db_table ="task_manager_subtask"
        verbose_name = "SubTask"
        verbose_name_plural = "SubTasks"
        ordering = ["-created_at"]


    def __str__(self):
        return self.title


class Category(models.Model):
    name: str = models.CharField(
        max_length=30,
        unique=True,
    )

    class Meta:
        db_table = "task_manager_category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
