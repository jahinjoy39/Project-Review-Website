from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Avg, Count
from projects.models import Project, Rating
from accounts.models import User

class StatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            'users': User.objects.count(),
            'projects': Project.objects.count(),
            'ratings': Rating.objects.count(),
            'average_rating': Rating.objects.aggregate(value=Avg('score'))['value'] or 0,
        })

class LeaderboardView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        top_projects = Project.objects.annotate(avg=Avg('ratings__score'), total=Count('ratings')).order_by('-avg', '-total')[:10]
        data = [
            {'project_id': p.id, 'title': p.title, 'average_score': round(p.avg or 0, 2), 'ratings_count': p.total}
            for p in top_projects
        ]
        return Response(data)
