from datetime import datetime

from django.db import models
from django.utils import timezone

from src.app.models.managers.category import SoftDeleteCategoryManager


class Category(models.Model):
    """Represents a category for tasks."""
    name: str = models.CharField(
        max_length=30,
        unique=True,
    )
    is_deleted: bool = models.BooleanField(default=False)
    deleted_at: datetime = models.DateTimeField(null=True)

    objects = SoftDeleteCategoryManager()

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.deleted_at = timezone.now()
        self.save()

    class Meta:
        """Meta options for the Category model."""
        db_table = "task_manager_category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
