from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from user.models import User


class Project(models.Model):
    name = models.CharField(max_length=30, null=False)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='project_creator')
    users = models.ManyToManyField(User)
    description = models.CharField(max_length=300, null=True, blank=True)
    priority = models.IntegerField(
        default=6,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=30, null=False)
    description = models.CharField(max_length=300, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    deadline = models.DateTimeField()

    def __str__(self):
        return self.name
