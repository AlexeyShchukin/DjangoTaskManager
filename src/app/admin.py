from django.contrib import admin

from src.app.models import Task, SubTask
from src.app.models.category import Category
from src.app.models.task import Status

admin.site.register(Category)


class SubTaskInline(admin.StackedInline):
    model = SubTask

    extra = 1


class BaseTaskAdmin(admin.ModelAdmin):
    list_display = (
        'short_title',
        'status',
        'created_at',
        'deadline',
        'status'
    )

    @admin.display(description='Title')
    def short_title(self, obj):
        if len(obj.title) > 10:
            return obj.title[:10] + "..."
        return obj.title


@admin.register(Task)
class TaskAdmin(BaseTaskAdmin):
    inlines = [SubTaskInline]


@admin.register(SubTask)
class SubTaskAdmin(BaseTaskAdmin):

    @admin.action(description='Mark as Done')
    def mark_done(self, request, queryset):
        updated = queryset.update(status=Status.DONE)

        self.message_user(request, f"{updated} subtasks marked as Done.")

    actions = [mark_done]
