from django.conf import settings
from django.db import models
from projects.models import Project


class Report(models.Model):
    TARGET_CHOICES = [
        ('project', 'Project'),
        ('feedback', 'Feedback'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports_made'
    )
    target_type = models.CharField(max_length=20, choices=TARGET_CHOICES)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='reports',
        null=True,
        blank=True
    )
    feedback_id = models.IntegerField(null=True, blank=True)
    reason = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reports_reviewed'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Report #{self.id} - {self.target_type}"