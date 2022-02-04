from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser


class FromContext(object):
    def __init__(self, value_fn):
        self.value_fn = value_fn

    def set_context(self, serializer_field):
        self.value = self.value_fn(serializer_field.context)

    def __call__(self):
        return self.value


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'first_name', 'last_name',
            'username', 'bio',
            'email', 'role',
        )
        model = CustomUser


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    title = serializers.HiddenField(
        default=FromContext(
            lambda context: context['request'].parser_context['kwargs']['title_id'])
    )

    class Meta:
        model = Review
        fields = ('pk', 'text', 'author', 'score', 'pub_date', 'title')
        read_only_fields = ('author', 'title')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
                message='Вы уже написали обзор на это произведение!'
            )
        ]

    def validate_score(self, value):
        if not (0 <= value <= 10):
            raise serializers.ValidationError(
                'Оценка должна быть в диапазоне от 0 до 10!')
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ('pk', 'text', 'author', 'pub_date')
        read_only_fields = ('author',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = ('name', 'year', 'rating', 'description', 'genre', 'category')
