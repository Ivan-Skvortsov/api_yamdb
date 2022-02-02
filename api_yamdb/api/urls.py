from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, GenreViewSet


v1_router = DefaultRouter()

v1_router.register(
    r'users', UserViewSet,
    basename='users'
)

v1_router.register(
    r'^genres', viewset=GenreViewSet
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
