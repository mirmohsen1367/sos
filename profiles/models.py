from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from profiles.custom_manager import CustomUserManager
from django.core.validators import RegexValidator


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=30, unique=True, validators=[RegexValidator(regex=r"^\d{10}$")]
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "username"

    objects = CustomUserManager()

    class Meta:
        db_table = "customuser"

    def __str__(self):
        return self.username
