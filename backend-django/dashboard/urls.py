from django.urls import path
from .views import StatsView, LeaderboardView
urlpatterns = [
    path('stats/', StatsView.as_view()),
    path('leaderboard/', LeaderboardView.as_view()),
]
