from pydoc import describe
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from useMyTime.user.models import User


class Project(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False)
    users = models.ManyToManyField(User)
    description = models.CharField(max_length=300, null=False)
    deadline = models.DateField()
    priority = models.IntegerField(
        default=6,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )

