from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Custom user model."""

    ROLES = [
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin')
    ]

    role = models.CharField(
        choices=ROLES,
        max_length=50,
        verbose_name='Роль пользователя',
        default='user',

    )
    email = models.EmailField(
        verbose_name='Email',
        help_text='Введите адрес электронной почты',
        unique=True
    )
    bio = models.TextField(
        verbose_name='О себе',
        help_text='Напиши что-нибудь о себе',
        null=True
    )
