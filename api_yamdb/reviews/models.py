from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    biography = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(verbose_name='Роль пользователя', max_length=50)
