from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from rest_framework.views import APIView
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title
from users.models import CustomUser
import api.filters as custom_filters
from api.permissions import IsAdmin, IsAdminOrReadOnly
from api.serializers import (CategorySerializer, CommentSerializer,
                             ConfirmationCodeSerializer, GenreSerializer,
                             ReviewSerializer, CreateUserSerializer,
                             TitleReadSerializer, TitleWriteSerializer,
                             UsersSerializer)


class CreateUserView(APIView):
    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            username = serializer.validated_data.get('username')
            user, _ = CustomUser.objects.get_or_create(
                email=email,
                username=username
            )
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                'Код подтверждения Yamdb',
                f'Ваш код подтверждения: {confirmation_code}',
                'admin@yamdb.ru',
                [email]
            )
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CheckTokenView(APIView):
    def post(self, request):
        serializer = ConfirmationCodeSerializer(data=request.data)
        if serializer.is_valid():
            confirmation_code = serializer.validated_data.get(
                'confirmation_code'
            )
            username = serializer.validated_data.get('username')
            user = get_object_or_404(CustomUser, username=username)
            if default_token_generator.check_token(user, confirmation_code):
                jwt_token = AccessToken.for_user(user)
                return Response(
                    f'Access Token: {str(jwt_token)}',
                    status=status.HTTP_200_OK
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    queryset = CustomUser.objects.all()
    search_fields = ('username',)

    @action(
        detail=False, methods=('get', 'patch',),
        url_path='me', url_name='me',
        permission_classes=(IsAuthenticated,)
    )
    def get_me(self, request):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(role=instance.role)
                return Response(serializer.data)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # TODO add custom permissions
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs["title_id"])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs["title_id"])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # TODO add custom permissions
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs["review_id"])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs["review_id"])
        serializer.save(author=self.request.user, review=review)


class GenreViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', ]
    lookup_field = 'slug'


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', ]
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = [IsAdminOrReadOnly, ]
    filterset_class = custom_filters.TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadSerializer
        return TitleWriteSerializer
