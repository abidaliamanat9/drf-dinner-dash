from django.db import models
from django.db.models import functions

from core.models import TimeStamped


class Hotel(TimeStamped):
    name = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name


class Category(TimeStamped):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                functions.Lower("name"),
                name="unique_category_name_ci"
            )
        ]
