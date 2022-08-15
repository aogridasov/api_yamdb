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
    confirmation_code = models.CharField(
        max_length=32,
        blank=True
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True,
    )

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == 'moderator' or self.is_superuser

    class Meta:
        db_table = 'auth_user'
