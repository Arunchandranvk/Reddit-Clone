from django.urls import path
from .views import *

urlpatterns = [
    path('communityadd/',CommunityAPIView.as_view(),name="community"),
    path('communities/<int:community_id>/', CommunityDetailAPIView.as_view(), name='community-detail'),
    path('communities/<int:community_id>/follow/', FollowCommunityAPIView.as_view(), name='follow-community'),
]