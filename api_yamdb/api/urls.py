from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet)

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

v1_router.register(
    r'titles/(?P<title_id>[\d]+)/reviews', ReviewViewSet,
    basename='reviews',
)

v1_router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet,
    basename='comments',
)


urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
