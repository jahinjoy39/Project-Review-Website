from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('presenter', 'Presenter'),
        ('reviewer', 'Reviewer'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='reviewer')
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
