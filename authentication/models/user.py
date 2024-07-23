from django.db import models
from django.contrib.auth.models import AbstractUser
from authentication.manager import UserManager


class User(AbstractUser):

    email = models.EmailField(unique=True, verbose_name='email', max_length=30)
    is_owner = models.BooleanField(default=False)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name', 'is_owner']

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

