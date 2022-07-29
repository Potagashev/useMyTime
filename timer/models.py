from django.db import models

from project.models import Task


class TaskTimer(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
