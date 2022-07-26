from django.db import models


class DirectionType(models.Model):
    abbreviation = models.CharField(max_length=10)
    explanation = models.CharField(max_length=100)


class ProjectType(models.Model):
    abbreviation = models.CharField(max_length=20)
    explanation = models.CharField(max_length=100)


class Order(models.Model):
    title = models.CharField(max_length=30, unique=True)
