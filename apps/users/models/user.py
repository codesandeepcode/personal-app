from .managers import UserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.models import BaseModel


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """Custom user model using email as the unique identifier."""

    email = models.EmailField(_("email address"), max_length=255, unique=True)
    name = models.CharField(_("name"), max_length=100, blank=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    is_admin = models.BooleanField(_("is admin"), default=False)
    is_staff = models.BooleanField(_("is staff"), default=False)
    is_superuser = models.BooleanField(_("is superuser"), default=False)
    use_2fa = models.BooleanField(_("use 2FA"), default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.email
