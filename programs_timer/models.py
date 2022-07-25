from django.db import models

from user.models import User


class Program(models.Model):
    name = models.CharField(max_length=30)


class ProgramTimer(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
