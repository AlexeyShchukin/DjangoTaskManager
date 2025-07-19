import os
import django
from django.db.models import Q
from django.utils.timezone import now, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()

from src.app.models import Task, SubTask

new_task = Task.objects.create(
    title="Prepare presentation",
    description="Prepare materials and slides for the presentation",
    status="New",
    deadline=now() + timedelta(days=3)
)

# new_task = Task.objects.get(pk=2)


subtasks = [
    SubTask(
        task=new_task,
        title="Gather information",
        description="Find necessary information for the presentation",
        status="New",
        deadline=now() + timedelta(days=2)
    ),
    SubTask(
        task=new_task,
        title="Create slides",
        status="New",
        deadline=now() + timedelta(days=1)
    )
]

SubTask.objects.bulk_create(subtasks)

new_tasks = Task.objects.filter(status="New")
print(new_tasks)

done_subtasks = SubTask.objects.filter(
    Q(status="Done") & Q(deadline__lt=now())
)

Task.objects.filter(title="Prepare presentation").update(status="in_progress")

SubTask.objects.filter(title="Gather information").update(deadline=now() - timedelta(days=2))

SubTask.objects.filter(title="Create slides").update(description="Create and format presentation slides")

Task.objects.filter(title="Prepare presentation").delete()
