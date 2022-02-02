from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, UserViewSet, GenreViewSet


v1_router = DefaultRouter()

v1_router.register(
    r'users', UserViewSet,
    basename='users'
)
v1_router.register(
    r'^genres', viewset=GenreViewSet
)
v1_router.register(
    r'^categories', viewset=CategoryViewSet
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
