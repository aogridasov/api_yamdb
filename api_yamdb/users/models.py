from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    confirmation_code = models.TextField(
        'Код подтверждения',
    )
    role = models.TextField()
    bio = models.TextField(blank=True)
    