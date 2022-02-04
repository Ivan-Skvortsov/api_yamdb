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


class CreateUserSerializer(serializers.ModelSerializer):

    def validate(self, data):
        username = data['username']
        if len(username) <= 2:
            raise serializers.ValidationError('Короткое имя пользователя')
        return data

    class Meta:
        model = CustomUser
        fields = ('email', 'username')


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=25, required=True)
    confirmation_code = serializers.CharField(required=True)


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
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
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
        fields = ('idgit ', 'text', 'author', 'pub_date')
        read_only_fields = ('author',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class TitleWriteSerializer(TitleReadSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
