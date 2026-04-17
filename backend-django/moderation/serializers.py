from rest_framework import serializers
from .models import Report
from projects.models import Project


class ReportSerializer(serializers.ModelSerializer):
    reporter_username = serializers.SerializerMethodField()
    reporter_id = serializers.SerializerMethodField()
    reviewed_by_username = serializers.SerializerMethodField()
    project_title = serializers.SerializerMethodField()

    project_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Report
        fields = [
            'id',
            'reporter',
            'reporter_id',
            'reporter_username',
            'target_type',
            'project',
            'project_title',
            'project_id',
            'feedback_id',
            'reason',
            'description',
            'status',
            'created_at',
            'reviewed_by',
            'reviewed_by_username',
            'reviewed_at',
        ]
        read_only_fields = [
            'reporter',
            'reporter_id',
            'reporter_username',
            'project',
            'project_title',
            'created_at',
            'reviewed_by',
            'reviewed_by_username',
            'reviewed_at',
        ]
        extra_kwargs = {
            'description': {'required': False, 'allow_blank': True},
            'feedback_id': {'required': False, 'allow_null': True},
        }

    def get_reporter_username(self, obj):
        return obj.reporter.username if obj.reporter else None

    def get_reporter_id(self, obj):
        return obj.reporter.id if obj.reporter else None

    def get_reviewed_by_username(self, obj):
        return obj.reviewed_by.username if obj.reviewed_by else None

    def get_project_title(self, obj):
        return obj.project.title if obj.project else None

    def validate(self, attrs):
        target_type = attrs.get('target_type')
        project_id = attrs.get('project_id')
        feedback_id = attrs.get('feedback_id')

        if target_type == 'project':
            if not project_id:
                raise serializers.ValidationError({
                    'project_id': 'project_id is required for project reports.'
                })

        if target_type == 'feedback':
            if not feedback_id:
                raise serializers.ValidationError({
                    'feedback_id': 'feedback_id is required for feedback reports.'
                })

        return attrs

    def create(self, validated_data):
        project_id = validated_data.pop('project_id', None)

        if project_id is not None:
            try:
                validated_data['project'] = Project.objects.get(id=project_id)
            except Project.DoesNotExist:
                raise serializers.ValidationError({
                    'project_id': 'Invalid project_id.'
                })

        return Report.objects.create(**validated_data)