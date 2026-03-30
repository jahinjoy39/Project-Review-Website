from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, RatingViewSet, CollaborationViewSet, SearchLogViewSet

router = DefaultRouter()
router.register(r'ratings', RatingViewSet, basename='rating')
router.register(r'collaborations', CollaborationViewSet, basename='collaboration')
router.register(r'search-logs', SearchLogViewSet, basename='searchlog')
router.register(r'', ProjectViewSet, basename='project')

urlpatterns = router.urls