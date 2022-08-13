from django.db import models
from django.contrib.auth.models import AbstractUser
from api_yamdb.settings import ROLE_CHOICES


class User(AbstractUser):
    role = models.CharField(
        max_length=9,
        choices=ROLE_CHOICES,
        default="user"
    )
    bio = models.TextField(
        verbose_name='bio',
        help_text='Напишите о себе',
        blank=True
    )

    class Meta:
        db_table = 'auth_user'
