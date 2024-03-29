from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    REQUIRED_FIELDS = [
        'displayName',
        'password',
        'first_name',
        'last_name',
        'email',
        'department',
        'appointment',
        'manager'
    ]
    displayName = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=False, null=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=False, null=False)
    email = models.EmailField(_("email address"), unique=True, blank=False, null=False)
    department = models.CharField(max_length=128, blank=False, null=False)
    appointment = models.CharField(max_length=128, blank=False, null=False)
    manager = models.ForeignKey("self", on_delete=models.SET_NULL, blank=False, null=True)
    photo = models.ImageField(blank=True, null=True, max_length=256, default=None)
    #
    # def __str__(self):
    #     return self.last_name, self.first_name
