from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Avg
from .models import Project, Rating, SearchLog, Collaboration
from .serializers import ProjectSerializer, RatingSerializer, SearchLogSerializer, CollaborationSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, 'creator', None) == request.user

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().select_related('creator')
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'top_rated']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsOwnerOrReadOnly()]

    def get_queryset(self):
        qs = self.queryset
        query = self.request.query_params.get('q')
        category = self.request.query_params.get('category')
        author = self.request.query_params.get('author')
        if query:
            if self.request.user.is_authenticated:
                SearchLog.objects.create(user=self.request.user, query=query)
            qs = qs.filter(Q(title__icontains=query) | Q(description__icontains=query))
        if category:
            qs = qs.filter(category__icontains=category)
        if author:
            qs = qs.filter(creator__username__icontains=author)
        return qs

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(detail=False, methods=['get'])
    def top_rated(self, request):
        projects = Project.objects.annotate(avg_score=Avg('ratings__score')).order_by('-avg_score')[:10]
        return Response(ProjectSerializer(projects, many=True, context={'request': request}).data)

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all().select_related('reviewer', 'project')
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

class CollaborationViewSet(viewsets.ModelViewSet):
    queryset = Collaboration.objects.all().select_related('user', 'project')
    serializer_class = CollaborationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SearchLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SearchLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SearchLog.objects.filter(user=self.request.user).order_by('-created_at')
