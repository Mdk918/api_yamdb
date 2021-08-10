from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Create your models here.


class User(AbstractUser):
    ROLE_ADMIN = 'admin'
    ROLE_MODERATOR = 'moderator'
    ROLE_USER = 'user'

    ROLE_CHOICES = {
        (ROLE_ADMIN, 'админ'),
        (ROLE_MODERATOR, 'модератор'),
        (ROLE_USER, 'юзер'),
    }

    email = models.EmailField('email address', unique=True)
    password = models.CharField('password', max_length=128, blank=True)
    biography = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(verbose_name='Роль пользователя', max_length=50,
                            default=ROLE_USER, choices=ROLE_CHOICES)

