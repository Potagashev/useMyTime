from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from project_properties.models import ProjectType, DirectionType
from user.models import User


class Order(models.Model):
    title = models.CharField(max_length=30, unique=True)


class Project(models.Model):
    name = models.CharField(max_length=30, null=False)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='project_creator')
    users = models.ManyToManyField(User)
    description = models.CharField(max_length=300, null=True, blank=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    type = models.ForeignKey(ProjectType, on_delete=models.SET_NULL, blank=True, null=True)
    direction_type = models.ForeignKey(DirectionType, on_delete=models.SET_NULL, blank=True, null=True)

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
    deadline = models.DateTimeField(null=True)

    def __str__(self):
        return self.name


