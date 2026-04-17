from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q, Avg
from .models import Project, Rating, SearchLog, Collaboration, HelpfulVote, Notification
from .serializers import (
    ProjectSerializer,
    RatingSerializer,
    SearchLogSerializer,
    CollaborationSerializer,
    NotificationSerializer,
)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, 'creator', None) == request.user


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().select_related('creator').prefetch_related('ratings__reviewer', 'ratings__helpful_votes')
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
        rating = serializer.save(reviewer=self.request.user)

        if rating.project.creator != self.request.user:
            Notification.objects.create(
                recipient=rating.project.creator,
                project=rating.project,
                message=f'{self.request.user.username} rated your project "{rating.project.title}" with score {rating.score}.'
            )


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


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-created_at')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def vote_helpful(request):
    user = request.user
    rating_id = request.data.get('rating_id')
    value = request.data.get('value')

    if value not in [1, -1, '1', '-1']:
        return Response(
            {'error': 'Value must be 1 for helpful or -1 for not helpful'},
            status=status.HTTP_400_BAD_REQUEST
        )

    value = int(value)

    try:
        rating = Rating.objects.get(id=rating_id)
    except Rating.DoesNotExist:
        return Response({'error': 'Rating not found'}, status=status.HTTP_404_NOT_FOUND)

    if rating.reviewer == user:
        return Response(
            {'error': 'You cannot vote on your own review'},
            status=status.HTTP_400_BAD_REQUEST
        )

    existing_vote = HelpfulVote.objects.filter(user=user, rating=rating).first()

    if existing_vote:
        return Response(
            {'error': 'You have already voted on this review'},
            status=status.HTTP_400_BAD_REQUEST
        )

    HelpfulVote.objects.create(user=user, rating=rating, value=value)

    if rating.reviewer != user:
        vote_text = 'helpful' if value == 1 else 'not helpful'
        Notification.objects.create(
            recipient=rating.reviewer,
            project=rating.project,
            message=f'{user.username} marked your review on "{rating.project.title}" as {vote_text}.'
        )

    return Response({
        'message': 'Vote recorded',
        'helpful_count': rating.helpful_votes.filter(value=1).count(),
        'not_helpful_count': rating.helpful_votes.filter(value=-1).count(),
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_read(request, notification_id):
    try:
        notification = Notification.objects.get(
            id=notification_id,
            recipient=request.user
        )
    except Notification.DoesNotExist:
        return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)

    notification.is_read = True
    notification.save()

    return Response({'message': 'Notification marked as read'})
