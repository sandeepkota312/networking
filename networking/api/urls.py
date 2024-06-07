from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
# router.register(r"userprofile", views.UserProfileViewSet, basename="userprofile")

urlpatterns = [
    path("", include(router.urls)),
]