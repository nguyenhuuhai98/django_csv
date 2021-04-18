from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Delete not use field
    username = None
    last_login = None
    is_staff = None
    is_superuser = None
    role = None

    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=10)
    address = models.TextField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.email
