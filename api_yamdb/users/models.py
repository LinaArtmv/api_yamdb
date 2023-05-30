from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Перепределили базовую модель User."""
    USER = 'USER'
    MODERATOR = 'MODERATOR'
    ADMIN = 'ADMIN'
    USER_ROLES = [(USER, 'user'),
                  (MODERATOR, 'moderator'),
                  (ADMIN, 'admin'), ]
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=9,
                            choices=USER_ROLES,
                            default=USER)

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __str__(self):
        return self.username
