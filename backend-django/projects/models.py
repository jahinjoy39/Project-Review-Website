from django.conf import settings
from django.db import models

class Project(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_projects')
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    upload = models.FileField(upload_to='projects/', blank=True, null=True)
    video_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Rating(models.Model):
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ratings')
    score = models.PositiveSmallIntegerField()
    clarity = models.PositiveSmallIntegerField(default=0)
    design = models.PositiveSmallIntegerField(default=0)
    research_depth = models.PositiveSmallIntegerField(default=0)
    technical_skill = models.PositiveSmallIntegerField(default=0)
    presentation_impact = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reviewer', 'project')

class SearchLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='search_logs')
    query = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Collaboration(models.Model):
    STATUS_CHOICES = [('invited', 'Invited'), ('accepted', 'Accepted'), ('removed', 'Removed')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='collaborations')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='collaborators')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='invited')

    class Meta:
        unique_together = ('user', 'project')
