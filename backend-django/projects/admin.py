from django.contrib import admin
from .models import Project, Rating, SearchLog, Collaboration
admin.site.register(Project)
admin.site.register(Rating)
admin.site.register(SearchLog)
admin.site.register(Collaboration)
