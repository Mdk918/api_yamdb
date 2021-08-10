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
    role = models.CharField(verbose_name='Роль пользователя', max_length=50)


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Категория')
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name='Жанр')
    slug = models.SlugField(unique=True, null=False)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Нзвание произведения')
    year = models.PositiveSmallIntegerField(
        verbose_name='Нзвание произведения'
    )
    description = models.TextField(verbose_name='Описание')
    genre = models.ForeignKey(Genre,
                              on_delete=models.CASCADE,
                              blank=True,
                              null=True,
                              related_name='titles',
                              verbose_name='Жанр')
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 blank=True,
                                 null=True,
                                 related_name='titles',
                                 verbose_name='Категория')

    def __str__(self):
        return self.name
