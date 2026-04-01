from rest_framework import serializers
from .models import Project, Rating, SearchLog, Collaboration
from accounts.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    average_score = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'category',
            'upload',
            'video_url',
            'creator',
            'created_at',
            'updated_at',
            'average_score',
        ]

    def get_average_score(self, obj):
        ratings = obj.ratings.all()
        if not ratings.exists():
            return 0
        return round(sum(r.score for r in ratings) / ratings.count(), 2)


class RatingSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'reviewer', 'project', 'score', 'created_at']


class SearchLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchLog
        fields = ['id', 'query', 'created_at']


class CollaborationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Collaboration
        fields = ['id', 'user', 'project', 'status']