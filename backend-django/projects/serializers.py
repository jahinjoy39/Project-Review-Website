from rest_framework import serializers
from .models import Project, Rating, SearchLog, Collaboration, HelpfulVote, Notification
from accounts.serializers import UserSerializer


class RatingSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)
    helpful_count = serializers.SerializerMethodField()
    not_helpful_count = serializers.SerializerMethodField()

    class Meta:
        model = Rating
        fields = [
            'id',
            'reviewer',
            'project',
            'score',
            'created_at',
            'helpful_count',
            'not_helpful_count',
        ]

    def get_helpful_count(self, obj):
        return obj.helpful_votes.filter(value=1).count()

    def get_not_helpful_count(self, obj):
        return obj.helpful_votes.filter(value=-1).count()


class ProjectSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    average_score = serializers.SerializerMethodField()
    ratings = RatingSerializer(many=True, read_only=True)

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
            'ratings',
        ]

    def get_average_score(self, obj):
        ratings = obj.ratings.all()
        if not ratings.exists():
            return 0
        return round(sum(r.score for r in ratings) / ratings.count(), 2)


class SearchLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchLog
        fields = ['id', 'query', 'created_at']


class CollaborationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Collaboration
        fields = ['id', 'user', 'project', 'status']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id',
            'message',
            'is_read',
            'created_at',
            'project',
        ]
