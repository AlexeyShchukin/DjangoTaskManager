from django.contrib import admin

from src.app.models import Task, SubTask, Category

admin.site.register(Task)
admin.site.register(SubTask)
admin.site.register(Category)

