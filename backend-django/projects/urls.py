from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet,
    RatingViewSet,
    CollaborationViewSet,
    SearchLogViewSet,
    NotificationViewSet,
    vote_helpful,
    mark_notification_read,
)

router = DefaultRouter()
router.register(r'ratings', RatingViewSet, basename='rating')
router.register(r'collaborations', CollaborationViewSet, basename='collaboration')
router.register(r'search-logs', SearchLogViewSet, basename='searchlog')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'', ProjectViewSet, basename='project')

urlpatterns = [
    path('vote-helpful/', vote_helpful),
    path('notifications/<int:notification_id>/read/', mark_notification_read),
] + router.urls
