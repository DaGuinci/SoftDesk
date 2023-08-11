from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
    age = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(120)],
        null=True
    )
    can_be_contacted = models.BooleanField(
        default=False
    )
    can_data_be_shared = models.BooleanField(
        default=False
    )
    created_time = models.DateTimeField(auto_now_add=True)


# TODO Faut il créer une classe spécifique Contributor