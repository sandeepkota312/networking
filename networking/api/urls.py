from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'friend-requests', views.FriendRequestViewSet, basename='friendrequest')
router.register(r'friends', views.FriendsNetworkViewSet, basename='friends')
# router.register(r'pending-requests', views.PendingFriendRequestsViewSet, basename='pendingrequests')

urlpatterns = [
    path('', include(router.urls)),
]