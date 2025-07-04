from datetime import datetime

from django.db import models
from django.db.models.functions import TruncDate


class Status(models.TextChoices):
    """Represents the possible statuses for tasks and subtasks."""
    NEW = "new", "New"
    IN_PROGRESS = "in_progress", "In Progress"
    PENDING = "pending", "Pending"
    BLOCKED = "blocked", "Blocked"
    DONE = "done", "Done"


class BaseTask(models.Model):
    """
    Abstract base model containing common fields for Task and SubTask.
    """
    title: str = models.CharField(
        max_length=200,
    )
    description: str = models.TextField(
        null=True,
        blank=True
    )
    status: str = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
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
        """Meta options for the BaseTask model."""
        abstract = True
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title


class Task(BaseTask):
    """
   Represents a main task with a title, description,
   categories, status, and deadline.
   """
    categories = models.ManyToManyField(
        'Category',
        related_name='tasks',
    )

    class Meta(BaseTask.Meta):
        """Meta options for the Task model."""
        db_table = "'task_manager_task'"
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        constraints = [
            models.UniqueConstraint(
                models.F('title'),
                TruncDate('created_at'),
                name='unique_task_title_per_day',
                violation_error_message="A task with this title already exists for this date."
            )
        ]


class SubTask(BaseTask):
    """Represents a sub-task, which is a part of a main Task."""
    title: str = models.CharField(
        max_length=200,
        unique=True
    )
    task = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE,
        related_name='subtasks',
        verbose_name="Parent Task"
    )

    class Meta(BaseTask.Meta):
        """Meta options for the SubTask model."""
        db_table = "task_manager_subtask"
        verbose_name = "SubTask"
        verbose_name_plural = "SubTasks"


class Category(models.Model):
    """Represents a category for tasks."""
    name: str = models.CharField(
        max_length=30,
        unique=True,
    )

    class Meta:
        """Meta options for the Category model."""
        db_table = "task_manager_category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
