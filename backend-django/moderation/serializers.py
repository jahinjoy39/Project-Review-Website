from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'reporter', 'project', 'reason', 'status', 'created_at']
        read_only_fields = ['reporter', 'status']
