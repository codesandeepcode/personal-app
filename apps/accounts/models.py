from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from apps.models import BaseModel
from .managers import CustomUserManager

class CustomUser(AbstractUser, BaseModel):
    username = None
    name = models.CharField(_("name"), max_length=100, unique=True)
    email = models.EmailField(_("email address"), max_length=100, unique=True)
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    is_admin = models.BooleanField("is admin", default=False)
    is_staff = models.BooleanField("is staff", default=False)
    is_superuser = models.BooleanField("is superuser", default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
