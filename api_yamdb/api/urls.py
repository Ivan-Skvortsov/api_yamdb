from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, TitleViewSet, UserViewSet, GenreViewSet,
                    send_email)


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
v1_router.register(
    r'^titles', viewset=TitleViewSet
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', send_email, name='signup')
]
