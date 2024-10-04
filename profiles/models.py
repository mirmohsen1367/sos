from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from profiles.custom_manager import CustomUserManager

# from django.core.validators import RegexValidator


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    first_name = models.CharField(null=True, blank=True, max_length=30)
    last_name = models.CharField(null=True, blank=True, max_length=30)
    email = models.EmailField(null=True, blank=True)
    date_joined = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "username"

    objects = CustomUserManager()

    class Meta:
        db_table = "customuser"

    def __str__(self):
        return self.username
