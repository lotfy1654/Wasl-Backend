from django.db import models


# Import AbstractUser
from django.contrib.auth.models import AbstractUser  , PermissionManager , Permission
from django.contrib.contenttypes.models import ContentType


ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
        ('User', 'User'),
    ]
    
class AllUsers(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default='User',
        null=True
    )
    date_joined = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.role == 'Admin':
            self.is_staff = True
            self.is_superuser = True
        elif self.role == 'Manager':
            self.is_staff = True
            self.is_superuser = False
        else:
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"
