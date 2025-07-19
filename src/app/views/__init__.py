from src.app.views.category import update_category, create_category
from src.app.views.task import get_all_tasks, create_task, get_task_by_id, get_statistic

__all__ = [
    "get_all_tasks",
    "create_task",
    "get_statistic",
    "get_task_by_id",

    "create_category",
    "update_category"
]
