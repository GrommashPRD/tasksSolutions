from django.db import transaction
from week_2.module_1.src.models import models


def fetch_task():
    with transaction.atomic():
        task = models.TaskQueue.objects.select_for_update().filter(status='pending').first()

        if task is not None:
            task.status = 'in_progress'
            task.save()
            return task
        return None