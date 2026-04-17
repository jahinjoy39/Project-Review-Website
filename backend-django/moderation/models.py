from django.conf import settings
from django.db import models
from projects.models import Project

class Report(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('reviewed', 'Reviewed'), ('dismissed', 'Dismissed')]
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='reports')
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
