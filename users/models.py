# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    profile_image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # Fixing the reverse accessor issue by providing a related_name
    groups = models.ManyToManyField('auth.Group', related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='customuser_permissions_set', blank=True)

    def __str__(self):
        return self.username
